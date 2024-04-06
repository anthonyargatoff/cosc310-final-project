import sqlite3
from flask import Blueprint, render_template, request, redirect, session, render_template

notifSub = Blueprint('notifSub', __name__)
database = "database.db"

# create new notification subscriptions
# @notifSub.route('/createNotification', methods=['GET','POST'])
# def addNotificaton():
#     if request.method == 'POST':
#         location = request.form.get('location')
#         longitude = request.form.get('longitude')
#         latitude = request.form.get('latitude')
#         radius = request.form.get('radius')
#         minMagnitude = request.form.get('minMagnitude')
#         maxMagnitude = request.form.get('maxMagnitude')
#         userID = session.get('userid')  # get user id from session
#         try:
#             sql = "INSERT INTO notification (location, longitude, latitude, radius, minMagnitude, maxMagnitude, userid) VALUES (?, ?, ?, ?, ?, ?, ?)"
#             data = (location, longitude, latitude, radius, minMagnitude, maxMagnitude, userID)
#             con = sqlite3.connect(database)
#             cursor = con.cursor()
#             cursor.execute(sql, data)
#             con.commit()
#             con.close()
#         except Exception as e:
#             print(e)
#     return render_template('/createNotification.html')

# view existing notification subscriptions
@notifSub.route('/viewNotifications', methods=['GET','POST'])
def viewNotifications():
    notifications = []
    try:
        userID = session.get('userid')  # get user id from session
        sql = "SELECT * FROM notification WHERE userid = %s"
        con = sqlite3.connect(database)
        cursor = con.cursor()
        cursor.execute(sql, (userID,))
        notifications = cursor.fetchall()
        con.close()
    except Exception as e:
        print(e)
    if notifications == []: #if notifications is empty
        notifications = "No notifications found"
    return render_template('viewNotifications.html',notifications=notifications)