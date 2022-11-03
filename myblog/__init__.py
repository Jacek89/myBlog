from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from myblog.extensions import db, ckeditor, bcrypt, login_manager, mail
from myblog.blueprints.auth import auth_bp
from myblog.blueprints.blog import blog_bp
from myblog.blueprints.admin import admin_bp
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['POSTS_PER_PAGE'] = 5

db.init_app(app)

migrate = Migrate(app, db)
moment = Moment(app)

login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'warning'

ckeditor.init_app(app)
bcrypt.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)



