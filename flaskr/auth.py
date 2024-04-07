import sqlite3
from flask import Blueprint, render_template, request, redirect, session

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
    # userID = session.get('userid')  # get user id from session 
    sql = "SELECT location, longitude, latitude, radius, minMagnitude, maxMagnitude FROM notification" # WHERE userid = %s"
    con = sqlite3.connect(database)
    cursor = con.cursor()
    cursor.execute(sql)
    notifications = cursor.fetchall()
    con.close()
    if notifications == []: #if notifications is empty
        notifications = "No notifications found"
    return render_template('viewNotifications.html',notifications=notifications)

connect = sqlite3.connect(database)
connect.execute("CREATE TABLE IF NOT EXISTS notification (notifyid INTEGER PRIMARY KEY AUTOINCREMENT,userid Integer,minMagnitude decimal(6, 4),maxMagnitude decimal(6, 4),latitude decimal(9, 6),longitude decimal(9, 6),location varchar(255),radius decimal(10, 6),Foreign Key (userid) References user(userid) On Delete Cascade On Update Cascade);")
                
