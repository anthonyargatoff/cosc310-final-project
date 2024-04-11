import sqlite3, json
from flask import Blueprint, flash, render_template, request, redirect, session

database = "database.db"
from .databaseClasses import DBManager as DBM
# create blueprint
auth = Blueprint('auth', __name__)

# database setup
userDB = DBM.DBUser('flaskr/main.db')

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
            if (userDB.validateAdmin(email, pw)):
                session['admin'] = True
            return redirect('/search')
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
        
        if userDB.validateUser(email, pw):
            # if login is successful, set the session to the user's email
            session['email'] = email
            session['password'] = pw
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

@auth.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('password', None)
    session.pop('admin', None)
    return render_template('logout.html')


# @auth.route('/signup', methods=['GET', 'POST'])
# def signup():
#      if request.method == 'POST':
#         #add database functionality here  
#         return redirect('/search')
#      return render_template('Signup.html')

@auth.route('/notifications')
def nottificationmanager_page():
    return render_template('manageNotifications.html')

@auth.route('/createNotification', methods=['POST'])
def nottificationcreator_page():
    createdNotification = False
    if request.method == 'POST':
        location, longitude, latitude, radius, minMagnitude, maxMagnitude = [request.form.get(key) for key in ['location', 'longitude', 'latitude', 'radius', 'minMagnitude', 'maxMagnitude']]
        #userID = session.get('userid')  # get user id from session
        message = ""
        try:
            sql = "INSERT INTO notification (location, longitude, latitude, radius, minMagnitude, maxMagnitude) VALUES (?, ?, ?, ?, ?, ?)"
            data = (location, longitude, latitude, radius, minMagnitude, maxMagnitude)
            con = sqlite3.connect(database)
            cursor = con.cursor()
            cursor.execute(sql, data)
            if cursor.rowcount > 0:
                createdNotification = True
                con.commit()
                con.close()
        except Exception as e:
            message += e.__str__()
        result = ""
        if (createdNotification):
            result = "Notification created successfully"
        else:
            result = "Failed to create notification - " + message
    return render_template('createNotification.html',result=result)

@auth.route('/viewNotifications', methods=['GET','POST'])
def viewNotifications():
    notifications = []
    # Currently shows all notifications in database. Once sessions is working, need to filter by user id
    # userID = session.get('userid')  # get user id from session 
    sql = "SELECT location, longitude, latitude, radius, minMagnitude, maxMagnitude FROM notification" # WHERE userid = %s"
    con = sqlite3.connect(database)
    cursor = con.cursor()
    cursor.execute(sql)
    notifications = cursor.fetchall()
    con.close()
    if notifications == []: #if notifications is empty
        notifications = "No notifications found"
    return render_template('viewNotifications.html',notifications=notifications,notifJSON=json.dumps(notifications))

connect = sqlite3.connect(database)
connect.execute("CREATE TABLE IF NOT EXISTS notification (notifyid INTEGER PRIMARY KEY AUTOINCREMENT,userid Integer,minMagnitude decimal(6, 4),maxMagnitude decimal(6, 4),latitude decimal(9, 6),longitude decimal(9, 6),location varchar(255),radius decimal(10, 6),Foreign Key (userid) References user(userid) On Delete Cascade On Update Cascade);")
                
