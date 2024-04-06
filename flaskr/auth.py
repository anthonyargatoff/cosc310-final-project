import sqlite3
from flask import Blueprint, render_template, request, redirect, session, render_template

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

@auth.route('/createNotification', methods=['GET','POST'])
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
            message = con.getconfig()
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

