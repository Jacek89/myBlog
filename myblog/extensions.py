from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_migrate import Migrate
from flask_gravatar import Gravatar
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
mail = Mail()
ckeditor = CKEditor()
bcrypt = Bcrypt()
oauth = OAuth()
moment = Moment()
migrate = Migrate()
gravatar = Gravatar(size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = 'warning'
