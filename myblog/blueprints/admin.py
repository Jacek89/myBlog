from flask import Blueprint, redirect, url_for, flash, render_template, abort
from flask_login import current_user
from myblog.forms import NewPostForm
from myblog.models import BlogPost, Comment
from myblog.extensions import db
from datetime import date
from functools import wraps

admin_bp = Blueprint("admin", __name__)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/new_post", methods=["GET", "POST"])
@admin_only
def create_post():
    if not current_user.is_authenticated:
        return redirect(url_for('blog.home'))
    form = NewPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
            body=form.body.data
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post successfully added.", "warning")
        return redirect(url_for("blog.home"))
    return render_template('new_post.html', form=form, title="Create Post")


@admin_bp.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = NewPostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for("blog.show_post", post_id=post.id))
    return render_template("new_post.html", form=form, edit_post=True, title="Edit Post")


@admin_bp.route("/delete_post/<int:post_id>")
@admin_only
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.home'))


@admin_bp.route("/delete_comment/<int:comment_id>")
@admin_only
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('blog.show_post', post_id=comment.post_id))
