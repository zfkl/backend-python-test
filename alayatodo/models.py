from alayatodo import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy(app)

Base = declarative_base()
engine = create_engine('sqlite:///alayacare.sqlite3', echo=True)
Session = sessionmaker(bind=engine)

class users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255))
    password = db.Column('password', db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class todos(db.Model):
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
