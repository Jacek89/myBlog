from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy.sql import func


db = SQLAlchemy()


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    post_comments = relationship("Comment", back_populates="commented_post")

    title = db.Column(db.Text, unique=True, nullable=False)
    subtitle = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text, nullable=False, default="user")
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, unique=True, nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")
    needs_rehash = db.Column(db.Boolean())


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    commented_post = relationship("BlogPost", back_populates="post_comments")
