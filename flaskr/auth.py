from flask import Blueprint, flash, render_template, request, redirect, session
from .databaseClasses import DBManager as DBM
import sqlite3
from flask import Blueprint, render_template, request, redirect, session

# create blueprint
auth = Blueprint('auth', __name__)

# database setup
userDB = DBM.DBUser('flaskr/main.db')

# routes 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # check for post request
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        id = userDB.selectUserId(email)
        if userDB.validateUser(email, pw):
            # if login is successful, set the session to the user's email
            session['email'] = email
            session['password'] = pw
            session['userid'] = id
            if (userDB.validateAdmin(email, pw)):
                session['admin'] = True
            return redirect('/search')
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
        
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('password', None)
    session.pop('admin', None)
    return render_template('logout.html')

@auth.route('/signup', methods =['GET', 'POST'])
def signup_page():
    # process the form data
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        cpw = request.form['confirm_password']

        # check if the password and confirm password match and if the email is already in use
        if hash(pw) != hash(cpw) and userDB.selectUserId(email) != False:
            return render_template('Signup.html')
        else:
            # else create a new user and redirect to login page with code 307
            userDB.addUser(email, pw, 0)
            session['email'] = email
            session['password'] = pw

            return redirect('/login', code=307)
    return render_template('Signup.html')


@auth.route('/admin')
def admin_page():
    return render_template('Admin.html')

@auth.route('/adminViewUsers')
def adminViewUsers_page():
    users, error = "", ""
    users = userDB.listUsers()
    if not users:
        error = "Failed to retrieve users : " + str(users)
    return render_template('adminViewUsers.html',users=users,error=error)

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


