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

# test if the data being sent to the client side js
# is the correct data
def test_data_points_sent(client):
    data_sent = {
        'Kelowna': [49.88, -119.49],
        'Vancouver': [49.28, -129.12],
        'some_data': 'Hello World!'
    }

    response = client.get('/send_data')
    res_data = response.get_json()

    for key, val in data_sent.items():
        assert key in res_data and val == res_data[key]

    assert response.status_code == 200
