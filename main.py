from flask import Flask, url_for, render_template, redirect, request, flash, abort
from models import db, BlogPost, User, Comment
from forms import RegisterForm, LoginForm, NewPostForm, CommentForm, ContactForm, ckeditor
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from datetime import date
from functools import wraps
from werkzeug.security import check_password_hash
from flask_moment import Moment
from flask_mail import Mail, Message
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
moment = Moment(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'warning'

ckeditor.init_app(app)
bcrypt = Bcrypt(app)

app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

# ################################ BASIC CONTENT ################################ #


@app.route("/")
@app.route("/home")
def home():
    posts = BlogPost.query.all()
    return render_template("index.html", posts=reversed(posts))


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/contact", methods=["GET", "POST"])
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
        return redirect(url_for('home'))
    return render_template("contact.html", form=form, title="Contact Me")

# ################################ POST HANDLING ################################ #


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    comment_form = CommentForm()
    if request.method == "POST" and comment_form.validate():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "warning")
            return redirect(url_for("login"))
        else:
            new_comment = Comment(
                text=comment_form.text.data,
                comment_author=current_user,
                commented_post=post
            )
            db.session.add(new_comment)
            db.session.commit()
    return render_template('post.html', post=post, comment_form=comment_form)


@app.route("/new_post", methods=["GET", "POST"])
@admin_only
def create_post():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for("home"))
    return render_template('new_post.html', form=form, title="Create Post")


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
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
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("new_post.html", form=form, edit_post=True, title="Edit Post")


@app.route("/delete_post/<int:post_id>")
@admin_only
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

# ################################ AUTHENTICATION ################################ #


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!", "danger")
            return render_template('register.html', form=form)
        if User.query.filter_by(name=form.username.data).first():
            flash(f"Username {form.username.data} is already taken", "danger")
            return render_template('register.html', form=form)
        secured_password = bcrypt.generate_password_hash(form.password.data, 15)
        new_user = User(
            email=form.email.data,
            password=secured_password,
            name=form.username.data,
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Successfully created user \"{form.username.data}\"", "warning")
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        # ######################## REHASHING IF NEEDED ##################### #
        if user and user.needs_rehash and check_password_hash(user.password, form.password.data):
            user.password = bcrypt.generate_password_hash(form.password.data)
            user.needs_rehash = False
            db.session.commit()
        # ################################################################## #
        if user and not user.needs_rehash and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Successfully logged in as {user.name}", "warning")
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash("Wrong email or password. Try again", "danger")
    return render_template('login.html', form=form, title="Login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out", "warning")
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
