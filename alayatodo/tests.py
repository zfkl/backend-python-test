from flask import (
    Flask,
    g,
    session
    )
from flask_testing import TestCase
from alayatodo import app


class ToDoViewTest(TestCase):


    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def login(self, username, password):
        """helper function as we need to test with authenticated users"""
        with app.test_client() as c:
            response = c.post('/login', follow_redirects=True, data=dict(username='user1', password='user1'))
        return response

    def logout(self):
        """helper function as we need to test if authenticated users can log out"""
        with app.test_client() as c:
            response = c.get('/logout', follow_redirects=True)
        return response

    def test_empty_description(self):
        """Empty string for description will trigger flash message and the
        placeholder presented to user will be changed to notify the latter
        """
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = ''
            response = c.post('/todo/', data=dict(description=description))
            self.assertEquals(response.status_code, 302)

    def test_valid_description_302(self):
        """OK test for a valid description, the table will be updated"""
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = 'valid string'
            response = c.post('/todo/', data=dict(description=description))
            self.assertEquals(response.status_code, 302)

    def test_description_404(self):
        """The response code should be 404 as this endpoint does not exist"""
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = 'test'
            response = c.post('/todo0/', data=dict(description=description))
            self.assertEquals(response.status_code, 404)

    def test_update_is_completed_302(self):
        """The response code should be 302: OK case for the update for this todo"""
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = 'test'
            response = c.post('/todo/%3Fis_completed%3DFalse%26id%3D1', data=dict(description=description))
            self.assertEquals(response.status_code, 302)

    def test_update_is_completed_unknown_task_404(self):
        """The response code should be 404: NOK case for the update for this unknown todo"""
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = 'test'
            response = c.post('/todo/%3Fis_completed%3DFalse%26id%3D1000', data=dict(description=description))
            self.assertEquals(response.status_code, 404)

    def test_update_is_completed_someone_else_task_401(self):
        """The response code should be 401: NOK case for the update of user 2 todo tast 6"""
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = 'test'
            response = c.post('/todo/%3Fis_completed%3DFalse%26id%3D6', data=dict(description=description))
            self.assertEquals(response.status_code, 401)

    def test_json_todo_404(self):
        """this todo doesnt exist 404 for response code"""
        with app.test_client() as c:
            log_response = c.post('/login', data=dict(username='user1', password='user1'))
            description = ''
            response = c.get('/todo/999999/json', data=dict(description=description))
            self.assertEquals(response.status_code, 404)
