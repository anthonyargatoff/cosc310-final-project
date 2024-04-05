import json
import pytest
from flask import request, url_for
from flaskr import create_app

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
        "email":"someone@example.com",
        "password":"1234"
    }

    response = client.get('/login')
    response = client.post('/login', data=form_data)

    # then check that redirect is made
    assert response.status_code == 302

# test the redirect to search page after signing up
def test_signup_redirect(client):
    form_data = {

    }
    response = client.post('/signup', data=form_data)
    assert response.status_code == 302

def test_login_redirect_follow(client):
    form_data = {
        "email":"someone@example.com",
        "password":"1234"
    }

    response = client.post('/login', data=form_data, follow_redirects=True)
    #assert len(response.history) == 1
    assert response.request.path == '/search'


# test if the data being sent to the client side js
# is the correct data
def test_data_points_sent(client):
    response = client.get('/search')
    res_data = response.get_json()

    assert response.status_code == 200
