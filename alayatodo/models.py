"""
Models for test app:
todos and users
each user has a list of todos that each can be read, deleted, updated and created
"""

from alayatodo import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255))
    password = db.Column('password', db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Todos(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    description = db.Column('description', db.String(255))
    is_completed = db.Column('is_completed', db.Integer)

    def __init__(self, user_id, description, is_completed):
        self.user_id = user_id
        self.description = description
        self.is_completed = is_completed

db.create_all()
db.session.commit()
