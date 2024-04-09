from flask import Blueprint, flash, render_template, request, redirect, session
from .databaseClasses import DBManager as DBM
# create blueprint
auth = Blueprint('auth', __name__)

# database setup
userDB = DBM.DBUser('main.db')

# routes 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # check for post request
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        
        if userDB.validateUser(email, pw):
            # if login is successful, set the session to the user's email
            return redirect('/search')
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
        
    return render_template('login.html')

@auth.route('/admin')
def admin_page():
    return render_template('Admin.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        confirmpw = request.form['confirm_password']
        User = userDB('main.db')
        if ((not User.validateUser()) and pw == confirmpw):
            User.addUser(email, pw, 0)

@auth.route('/account')
def accountmanager_page():
    return render_template('manageAccount.html')

@auth.route('/notifications')
def nottificationmanager_page():
    return render_template('manageNotifications.html')

