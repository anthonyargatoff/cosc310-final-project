from flask import Blueprint, render_template, request, redirect, session
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
        print(email, pw)
        # need to figure out how to access the remember me checkbox
        # next steps are to incorporate the database and setup credential validation
        # from here redirect to the main page which is search page
        # next steps for the redirect would be to include a payload to dynamically display public user data like their username
        return redirect('/search')
        
    return render_template('login.html')

@auth.route('/admin')
def admin_page():
    return render_template('Admin.html')

@auth.route('/signup', methods =['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        cpw = request.form['confirm_password']

        if hash(pw) != hash(cpw):
            return render_template('Signup.html')
        else:
            userDB.addUser(email, pw, 0)
            return redirect('/login', code=307)
    return render_template('Signup.html')

@auth.route('/account')
def accountmanager_page():
    return render_template('manageAccount.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
        #add database functionality here  
        return redirect('/search')
     return render_template('Signup.html')

@auth.route('/notifications')
def nottificationmanager_page():
    return render_template('manageNotifications.html')

