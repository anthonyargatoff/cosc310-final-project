from flask import Blueprint, render_template, redirect, request, jsonify
import sqlite3

view = Blueprint('view', __name__)

@view.route('/eventAPI', methods = ['GET'])
def eventAPI():
    startTime = request.args.get('starttime', default='2022-03-01', type=str)
    endTime = request.args.get('endtime', default='2022-04-01', type=str)
    minMagnitude = request.args.get('minmagnitude', default=0, type= float)
    maxMagnitude = request.args.get('maxmagnitude', default=10, type = float)

    try:
        con = sqlite3.connect("flaskr/main.db")
        cursor = con.cursor()
        params = (startTime, endTime, minMagnitude, maxMagnitude)
        SQL = "SELECT title, eventTime, magnitude, latitude, longitude, depth, url FROM earthquake WHERE eventTime BETWEEN ? AND ? AND magnitude BETWEEN ? AND ? ORDER BY eventTime ASC;"
        cursor.execute(SQL, params)
        # cursor.execute(SQL)
        rows = cursor.fetchall()
        con.commit()
        con.close()

        events = []
        for row in rows:
            event = {
                'title': row[0],
                'eventTime': row[1],
                'magnitude': row[2],
                'latitude': row[3],
                'longitude': row[4],
                'depth': row[5], 
                'url': row[6]
            }
            events.append(event)

        response = {'events': events}
        return jsonify(response)
        # return startTime + endTime + " " + str(minMagnitude) + " "  + str(maxMagnitude)
    
    except Exception as e:
        return jsonify({'error': str(e)})

@view.route('/search')
def search():
    return render_template('Search.html')

@view.route('/landing')
def landing_page():
    return render_template('Landing.html')

@view.route('/about')
def about_page():
    return render_template('About.html')