from flask import (
    Flask,
    g,
    session
    )
from flask_testing import TestCase
import sqlite3
from alayatodo import app

DATABASE = 'C:\Users\zfk\AppData\Local\Temp\\alayatodo_tests.db'


class ToDoViewTest(TestCase):


    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def login(self, username, password):
        with app.test_client() as c:
            response = c.post('/login', data=dict(username='user1', password='user1'))
        return response

    def logout(self):
        with app.test_client() as c:
            response = c.get('/logout', follow_redirects=True)
        return response

    def test_empty_description(self):
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = ''
            response = c.post('/todo/', data=dict(description=description))
            self.assertEquals(response.status_code, 302)

    def test_json_todo_404(self):
        """this todo doesnt exist 404 for response code"""
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = ''
            response = c.get('/todo/999999/json', data=dict(description=description))
            self.assertEquals(response.status_code, 404)
