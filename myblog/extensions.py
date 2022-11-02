from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
mail = Mail()
ckeditor = CKEditor()
login_manager = LoginManager()
bcrypt = Bcrypt()
