"""
Init app
set config from environment variables for secuity
"""
import os
import sqlite3

from flask import Flask, g


# configuration
# DATABASE = 'C:\Users\zfk\AppData\Local\Temp\\alayatodo.db'
# SQLITE = 'sqlite:///alayacare_.sqlite3'
DATABASE = os.getenv('database', 'C:\Users\zfk\AppData\Local\Temp\\alayatodo.db')
DEBUG = os.getenv('DEBUG', False)
SECRET_KEY = os.getenv('development key', 'test')
USERNAME = os.getenv('admin')
PASSWORD = os.getenv('default')
MAX_PER_PAGE = os.getenv('MAX_PER_PAGE', 10)

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLAlchemy_URI', 'sqlite:///alayacare_.sqlite3')
app.config['TODO_PER_PAGE'] = MAX_PER_PAGE


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


import alayatodo.views