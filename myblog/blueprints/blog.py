from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user
from flask_mail import Message
from myblog.models import BlogPost, Comment
from myblog.forms import ContactForm, CommentForm
from myblog.extensions import db, mail
import os

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
@blog_bp.route("/home")
def home():
    posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
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
        msg = Message('Hello from MyBlog Contact Form', sender=os.environ.get("MAIL_USER"),
                      recipients=[os.environ.get("MAIL_USER")])
        msg.body = f"""
        Name: {form.name.data}
        E-Mail: {form.email.data}

        Message: {form.text.data}"""
        mail.send(msg)
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
