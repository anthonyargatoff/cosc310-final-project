from flask import Blueprint, render_template, redirect, request, jsonify
import sqlite3

view = Blueprint('view', __name__)


@view.route('/send_data', methods = ['GET'])
def send_data():

    return jsonify({'events': [{
    'title':'Kelowna earthquake',
    'latitude':49.9,
    'longitude':-119.4,
    'magnitude':4.67,
    'URL': "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=1568-01-01&endtime=1568-01-31"
    },
    {
    'title':'Vancouver earthquake',
    'latitude':49.45,
    'longitude':-121.34,
    'magnitude':5.67,
    'URL': "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=1568-01-01&endtime=1568-01-31"
    }]})

@view.route('/eventAPI', methods = ['GET'])
def eventAPI():
    startTime = request.args.get('starttime', default='2022-02-01', type=str)
    endTime = request.args.get('endtime', default='2022-03-01', type=str)
    minMagnitude = request.args.get('minmagnitude', default=0, type= float)
    maxMagnitude = request.args.get('maxmagnitude', default=10, type = float)

    try:
        con = sqlite3.connect("flaskr/main.db")
        cursor = con.cursor()
        params = (startTime, endTime, minMagnitude, maxMagnitude)
        SQL = "SELECT title, eventTime, magnitude, latitude, longitude, depth, url FROM earthquake WHERE eventTime BETWEEN ? AND ? AND magnitude BETWEEN ? AND ? ORDER BY eventTime DESC;"
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