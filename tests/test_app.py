import json
import pytest
from flask import request, url_for, session
from flaskr import create_app
from flaskr.databaseClasses import DBManager as DBM

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_login_form_redirect(client):
    form_data = {
        "email":"someone2@example.com",
        "password":"1234"
    }

    response = client.get('/login')
    response = client.post('/login', data=form_data)

    # then check that redirect is made
    assert response.status_code == 302

# test the redirect to search page after signing up
# proper signup
def test_signup_redirect(client):
    db = DBM.DBUser('flaskr/main.db')
    form_data = {
        "email":"someone3@example.com",
        "password":"1234",
        "confirm_password":"1234"
    }
    response = client.post('/signup', data=form_data, follow_redirects=True)

    #assert response.status_code == 307
    assert response.request.path == '/login'
    x = db.selectUserId('someone3@example.com')
    assert x is not False
    db.deleteUser('someone3@example.com')



def test_login_redirect_follow(client):
    form_data = {
        "email":"someone2@example.com",
        "password":"1234"
    }

    response = client.post('/login', data=form_data, follow_redirects=True)
    #assert len(response.history) == 1
    assert response.request.path == '/search'

def test_logout(client):

    # first login
    form_data = {
        "email":"someone2@example.com",
        "password":"1234"
    }

    response = client.post('/login', data=form_data, follow_redirects=True)

    # then logout
    response = client.get('/logout', follow_redirects=True)
    assert response.request.path == '/logout'
    assert response.status_code == 200

def test_admin_login(client):
    form_data = {
        "email":"test@hotmail.com",
        "password":"test"
    }

    with client:
        response = client.post('/login', data=form_data, follow_redirects=True)
        assert session['admin'] == True

def test_search(client):
    pass

def test_add_notification(client):
    pass

def test_remove_notification(client):
    pass


