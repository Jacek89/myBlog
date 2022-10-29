from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_ckeditor import CKEditorField, CKEditor

ckeditor = CKEditor()


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=8), EqualTo('password', message='Entered passwords do not match')]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class NewPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    img_url = StringField("Image URL", validators=[DataRequired()])
    subtitle = TextAreaField("Subtitle", validators=[DataRequired(), Length(max=1000)])
    body = CKEditorField("Body", validators=[DataRequired()])
    submit = SubmitField("Add Post")


class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField("Add Comment")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    text = TextAreaField("Message", validators=[DataRequired(), Length(max=10000)])
    submit = SubmitField("Send")
