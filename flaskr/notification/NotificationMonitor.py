import flaskr.databaseClasses.NotificationManager as NM
from flaskr.notification.Notification import Notification
from flaskr.notification.sendEmail import send_email

class Notificationmonitor:
    """
    hadndles notification sending
    """
    def __init__(self, databasepath):
        """Initialization

        Args:
            databasepath (String): Path to the database
        """
        self.Notifications = [];
        self.database = databasepath;
        self.loadNotify();

    def notifyAll(self, Events):
        """Sends notifications to all that qualify

        Args:
            Events (List<dict>): List of events organized by dicts with keys magnitude, latitude, longitude
        """
        for notif in self.Notifications:
            sendEvents = [];
            for event in Events:
                if notif['Notification'].compareNewEvent(event['magnitude'],event['latitude'],event['longitude']):
                    sendEvents.append(event);
            msgBody = '';
            if len(sendEvents) > 0:
                for event in sendEvents:
                    msgBody + '\n Magnitude: {} lat: {} long: {}'.format(event['magnitude'], event['latitude'], event['longitude'])
                body = "A new event has triggered your notification settings." + msgBody
                send_email(body, notif['email'])

    def loadNotify(self):
        """Load notifications from database
        """
        manager = NM.DBNotification(self.database)
        Notifications = manager.getAllNotifications()
        list = [];
        for notif in Notifications:
            n = Notification(notif[1])
            list.append({'Notification':n , 'email': notif[2]})
        self.Notifications = list;
