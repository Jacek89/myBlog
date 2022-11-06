from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app
from flask_login import current_user
from myblog.models import BlogPost, Comment
from myblog.forms import ContactForm, CommentForm
from myblog.extensions import db
from myblog.emails import send_mail
import os

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
@blog_bp.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts_per_page = current_app.config['POSTS_PER_PAGE']
    posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=posts_per_page)
    return render_template("index.html", posts=posts)


@blog_bp.route("/about")
def about():
    return render_template("about.html", title="About")


@blog_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if current_user.is_authenticated:
        form = ContactForm(name=current_user.name, email=current_user.email)
    else:
        form = ContactForm()

    if form.validate_on_submit():
        send_mail(
            subject='Hello from MyBlog Contact Form',
            to=os.environ.get("MAIL_USER"),
            body=f'''
            Name: {form.name.data}
            E-mail: {form.email.data}
            Message: {form.text.data}'''
        )
        flash("Thank You for your message.", "warning")
        return redirect(url_for('blog.home'))
    return render_template("contact.html", form=form, title="Contact Me")


@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    comment_form = CommentForm()
    if request.method == "POST" and comment_form.validate():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "warning")
            return redirect(url_for("auth.login"))
        else:
            new_comment = Comment(
                text=comment_form.text.data,
                comment_author=current_user,
                commented_post=post
            )
            db.session.add(new_comment)
            db.session.commit()
    return render_template('post.html', post=post, comment_form=comment_form)
