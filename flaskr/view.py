from flask import Blueprint, render_template, redirect, request, jsonify
import sqlite3
from flaskr.distanceBetweenPoints.distanceBetweenPoints import coordinateCalculator

view = Blueprint('view', __name__)

@view.route('/eventAPI', methods = ['GET'])
def eventAPI():
    startTime = request.args.get('startdate', default='2022-03-01', type=str)
    endTime = request.args.get('enddate', default='2022-03-02', type=str)
    minMagnitude = request.args.get('minmagnitude', default=0, type= float)
    maxMagnitude = request.args.get('maxmagnitude', default=10, type = float)
    latitude = request.args.get('latitude', default=None, type= float)
    longitude = request.args.get('longitude', default=None, type=float)
    radius = request.args.get('radius', default=None, type=float)

    try:
        con = sqlite3.connect("flaskr/main.db")
        cursor = con.cursor()
        params = (startTime, endTime, minMagnitude, maxMagnitude)
        SQL = "SELECT title, eventTime, magnitude, latitude, longitude, depth, url FROM earthquake WHERE eventTime BETWEEN ? AND ? AND magnitude BETWEEN ? AND ? ORDER BY eventTime ASC;"
        cursor.execute(SQL, params)
        rows = cursor.fetchall()
        con.commit()
        con.close()

        events = []
        for row in rows:
            if (latitude and longitude and radius):
                if (coordinateCalculator.getDistanceKilometers(latitude, longitude, float(row[3]), float(row[4])) <= radius):
                    print('test')
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

            else:
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
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@view.route('/eventAPIcount', methods = ['GET'])
def eventAPIcount():
    startTime = request.args.get('startdate', default='2022-03-01', type=str)
    endTime = request.args.get('enddate', default='2022-03-02', type=str)
    minMagnitude = request.args.get('minmagnitude', default=0, type= float)
    maxMagnitude = request.args.get('maxmagnitude', default=10, type = float)
    latitude = request.args.get('latitude', default=None, type= float)
    longitude = request.args.get('longitude', default=None, type=float)
    radius = request.args.get('radius', default=None, type=float)

    try:
        con = sqlite3.connect("flaskr/main.db")
        cursor = con.cursor()
        params = (startTime, endTime, minMagnitude, maxMagnitude)
        SQL = "SELECT title, eventTime, magnitude, latitude, longitude, depth, url FROM earthquake WHERE eventTime BETWEEN ? AND ? AND magnitude BETWEEN ? AND ? ORDER BY eventTime ASC;"
        print(startTime+ " " + endTime)
        cursor.execute(SQL, params)
        # cursor.execute(SQL)
        rows = cursor.fetchall()
        con.commit()
        con.close()

        events = []
        for row in rows:
            if (latitude and longitude and radius):
                if (coordinateCalculator.getDistanceKilometers(latitude, longitude, float(row[3]), float(row[4])) <= radius):
                    print('test')
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

            else:
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

        numEvents = len(events)            
        response = {'count': numEvents}
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@view.route('/search')
def search():
    return render_template('Search.html')

@view.route('/landing')
def landing_page():
    return render_template('Landing.html')

@view.route('/about')
def about_page():
    return render_template('About.html')

@view.route('/account')
def account_management_page():
    return render_template('accountManagement.html')