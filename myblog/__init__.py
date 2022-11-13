from flask import Flask
from myblog.config import Config
from myblog.extensions import db, ckeditor, bcrypt, login_manager, mail, oauth, moment, migrate, gravatar
from myblog.blueprints.auth import auth_bp
from myblog.blueprints.blog import blog_bp
from myblog.blueprints.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    bcrypt.init_app(app)
    oauth.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    gravatar.init_app(app)

    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

    return app
