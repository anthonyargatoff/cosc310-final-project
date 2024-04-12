from flask import Blueprint, render_template, request, redirect, session
from .databaseClasses import DBManager as DBM
import sqlite3
userDB = DBM.DBUser('flaskr/main.db')
database = "database.db"

notifications = Blueprint('notifications', __name__)

@notifications.route('/hello')
def hello():
    return '<h1>Hello World</h1><script>alert("hello world!");</script>'

@notifications.route('/viewNotifications', methods=['GET','POST'])
def viewNotifications():
    notifications, error = [], ""
    userID = session.get('userid')
    if (userID == None):
        return redirect('/login', code=307)
    else:
        notifications = userDB.getNotificationList(userID)
        if notifications == []: #if notifications is empty
            error = "No notifications found"
        return render_template('viewNotifications.html',notifications=notifications, userID=userID,error=error)
    
@notifications.route('/createNotification', methods=['POST'])
def nottificationcreator_page():
    id = session.get('userid')
    if (id == None):
        return redirect('/login', code=307)
    else:
        if request.method == 'POST':
            attributes = "magnitude:"+str(request.form.get('minMagnitude')) + "-" + str(request.form.get('maxMagnitude')) +";area:"+ str(request.form.get('latitude')) +","+ str(request.form.get('longitude')) +","+ str(request.form.get('radius'))
            if (userDB.addNotification(id, attributes)):
                result = "Notification created successfully"
            else:
                result = "Failed to create notification"
        return render_template('createNotification.html',result=result)