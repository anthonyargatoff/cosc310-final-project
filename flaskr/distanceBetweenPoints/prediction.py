
import sqlite3
from flaskr.distanceBetweenPoints.distanceBetweenPoints import coordinateCalculator
from operator import itemgetter

import requests
from datetime import date
from datetime import timedelta


class predictionCalculator():

    @staticmethod
    def getEventsDB(startDate, endDate):
        """Gets all events in date range from main.db 

        Args:
            startDate (String): _description_
            endDate (String): _description_

        Returns:
            _type_: list of events with latitude and longitude keys for each event
        """
        con = sqlite3.connect("../main.db");
        cursor = con.cursor();
        params = (startDate, endDate)
        SQL = "Select latitude, longitude From earthquake Where eventTime Between ? and ?;";
        cursor.execute(SQL, params);
        rows = cursor.fetchall();
        con.commit();
        con.close();

        events = [];
        for row in rows:
            event = {'latitude': row[0], 'longitude': row[1]};
            events.append(event)
        return events;

    @staticmethod
    def getEventsAPI():
        """Gets all events in last 4 days from API 

        Returns:
            _type_: list of events with latitude and longitude keys for each event from API
        """

        url = 'https://earthquake.usgs.gov/fdsnws/event/1/'
        #https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02

        events = []
        response = requests.get("{}query?format=geojson&starttime={}&endtime={}".format(url, (date.today() - timedelta(days = 4)), date.today())).json()

        for feature in response["features"]:
            geometry = feature["geometry"]
            longitude = geometry["coordinates"][0]
            latitude = geometry["coordinates"][1]

            event = {"latitude":latitude, "longitude":longitude}
            events.append(event)
        return events

    @staticmethod
    def getPredictions(events, radius = 200):
        """_summary_

        Args:
            events (List<Events>): List of events with latitude and longitude keys
            radius (number):    Radius (in km) around which to conduct the search, default 100.

        Returns:
            _type_: List of predictions (length < 10), have latitude and longitude keys, as well as a count key
                        for the number of events nearby.
        """
        processedEvents = [];
        for event in events:
            reference = event;
            count = 0;
            for eachevent in events:
                if coordinateCalculator.getDistanceKilometers(reference['latitude'],reference['longitude'],eachevent['latitude'],eachevent['longitude']) < radius:
                    count = count+1;
            processedEvents.append({'latitude': reference['latitude'], 'longitude': reference['longitude'], 'count':count});

        sortedarr = sorted(processedEvents, key=itemgetter('count'), reverse=True);
        output = [];
        for processedEvent in sortedarr:
            valid = True;
            for eachevent in output:
                if coordinateCalculator.getDistanceKilometers(processedEvent['latitude'],processedEvent['longitude'],eachevent['latitude'],eachevent['longitude']) < radius:
                    valid = False;
            if valid:
                finalEvent = {'latitude': processedEvent['latitude'], 'longitude': processedEvent['longitude'], 
                              'count':processedEvent['count'], 'rank': (len(output)+1), 'description': 'Placeholder desc'}
                output.append(finalEvent);
            if len(output) > 9:
                return output;
        return output;

