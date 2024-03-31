from flask import Blueprint

notifications = Blueprint('notifications', __name__)

@notifications.route('/hello')
def hello():
    return '<h1>Hello World</h1><script>alert("hello world!");</script>'