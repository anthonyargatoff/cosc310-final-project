
import sqlite3
from distanceBetweenPoints import coordinateCalculator
from operator import itemgetter

class predictionCalculator():

    @staticmethod
    def getEvents(startDate, endDate):
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
    def getPredictions(events, radius = 100):
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
                output.append(processedEvent);
            if len(output) > 9:
                return output;
        return output;

'''
get point i of n from database.
variable iPoints to hold number of points found
compare it with all other database items, i2, i3, i4, ..., in
if $in$ is in the radius, add +1 to iPoints
repeat for each point in db
return the top 10 points that do not overlap with each other
'''