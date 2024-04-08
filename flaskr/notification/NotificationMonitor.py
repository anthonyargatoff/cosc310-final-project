import flaskr.notification.NotificationManager as NM
from flaskr.notification.Notification import Notification
from flaskr.notification.sendEmail import send_email

class Notificationmonitor:
    """
    
    """
    def __init__(self, databasepath):
        """
        Initialization.

        """
        self.Notifications = [];
        self.database = databasepath;
        self.loadNotify();

    def notifyAll(self, Events):
        for notif in self.Notifications:
            for event in Events:
                if notif['Notification'].compareNewEvent(event['magnitude'],event['latitude'],event['longitude']):
                    body = """A new event has triggered your notification settings. 
                    \n Magnitude: {}
                    \n lat: {}
                    \n long: {}                    
                    """.format(event['magnitude'], event['latitude'], event['longitude'])
                    send_email(body, notif['email'])

    def loadNotify(self):
        manager = NM.DBNotification(self.database)
        Notifications = manager.getAllNotifications()
        list = [];
        for notif in Notifications:
            n = Notification(notif[1])
            list.append({'Notification':n , 'email': notif[2]})
        self.Notifications = list;
