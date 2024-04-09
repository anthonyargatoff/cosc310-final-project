from flaskr.notification.NotificationMonitor import Notificationmonitor
import requests
from datetime import datetime
from datetime import timedelta


def handleNotifications():
    """Fetches last 5 mins from API, then hands them to the notification monitor
    """
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/'
    events = []
    response = requests.get("{}query?format=geojson&starttime={}&endtime={}".format(url, (datetime.today() - timedelta(minutes = 5)), datetime.today())).json()

    for feature in response["features"]:
        properties = feature["properties"]
        mag = properties["mag"]
        geometry = feature["geometry"]
        longitude = geometry["coordinates"][0]
        latitude = geometry["coordinates"][1]

        event = {"magnitude":mag, "latitude":latitude, "longitude":longitude}
        events.append(event)

    NM = Notificationmonitor('flaskr/main.db')
    NM.notifyAll(events)
