import sqlite3, json, sys
from flask import Blueprint, render_template, request, redirect, session
sys.path.insert(0, 'flaskr')
from databaseClasses.DBManager import DBUser

database = "database.db"

# create blueprint
auth = Blueprint('auth', __name__)

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
         return redirect('/search')
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

@auth.route('/adminViewUsers')
def adminViewUsers_page():
    users, error = "", ""
    User = DBUser(database)
    users = User.listUsers()
    if not users:
        error = "Failed to retrieve users : " + str(users)
    return render_template('adminViewUsers.html',users=users,usersJSON=json.dumps(users),error=error)

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
