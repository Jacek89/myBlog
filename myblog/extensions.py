from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
mail = Mail()
ckeditor = CKEditor()
bcrypt = Bcrypt()
oauth = OAuth()
moment = Moment()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = 'warning'
