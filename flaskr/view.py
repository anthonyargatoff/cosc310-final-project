from flask import Blueprint, render_template, redirect, request, jsonify

view = Blueprint('view', __name__)


@view.route('/send_data', methods = ['GET'])
def send_data():
    return jsonify({'some_data': 'Hello World!', 'Kelowna': [49.88, -119.49], 'Vancouver': [49.28, -129.12]})

@view.route('/search')
def search():
    return render_template('Search.html')

@view.route('/landing')
def landing_page():
    return render_template('Landing.html')

@view.route('/about')
def about_page():
    return render_template('About.html')

@view.route('/account')
def account_management_page():
    return render_template('accountManagement.html')