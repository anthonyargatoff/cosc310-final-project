from flask import Blueprint, flash, render_template, request, redirect, session
from .databaseClasses import DBManager as DBM
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
        
        if userDB.validateUser(email, pw):
            # if login is successful, set the session to the user's email
            session['email'] = email
            session['password'] = pw
            session['loggedin'] = True
            if (userDB.validateAdmin(email, pw)):
                session['admin'] = True
            return redirect('/search')
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
        
    return render_template('login.html')


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

