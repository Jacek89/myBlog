from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from myblog.models import User
from myblog.forms import RegisterForm, LoginForm
from myblog.extensions import db, bcrypt, login_manager
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("You've already signed up with that email, log in instead!", "danger")
            return render_template('register.html', form=form)
        if User.query.filter_by(name=form.username.data).first():
            flash(f"Username {form.username.data} is already taken", "danger")
            return render_template('register.html', form=form)
        secured_password = bcrypt.generate_password_hash(form.password.data, 15).decode('utf-8')
        new_user = User(
            email=form.email.data.lower(),
            password=secured_password,
            name=form.username.data,
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Successfully created user \"{form.username.data}\"", "warning")
        return redirect(url_for('blog.home'))
    return render_template('register.html', form=form, title="Register")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data.lower()).first()
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
                return redirect(url_for('blog.home'))
        else:
            flash("Wrong email or password. Try again", "danger")
    return render_template('login.html', form=form, title="Login")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out", "warning")
    return redirect(url_for('blog.home'))
