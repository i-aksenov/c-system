from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255))
    question_answer = db.Column(db.String(80))
    perm_read_private_docs = db.Column(db.Boolean, default=False)
    perm_give_out_food = db.Column(db.Boolean, default=False)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    path = db.Column(db.String(200))


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    coupon = db.Column(db.String(100), nullable=False)
