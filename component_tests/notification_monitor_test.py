
import unittest;
from flaskr.notification.NotificationMonitor import Notificationmonitor

class test_DBManager(unittest.TestCase):

    def setUp(self):
        self.NM = Notificationmonitor('component_tests/testdata/testSendNotify.db');

    def testLoadNotify(self):
        self.NM.loadNotify()
        self.assertEqual(len(self.NM.Notifications),1)
        self.assertEqual(self.NM.Notifications[0]['email'], 'ryanpybus8596@gmail.com')
        self.assertEqual(self.NM.Notifications[0]['Notification'].radius, 10000)

    def testNotifyAll(self):
        self.NM.notifyAll([{'magnitude':5 , 'latitude': 50, 'longitude': 100},{'magnitude':2 , 'latitude': -50, 'longitude': -100}])

    def tearDown(self):
        self.NM = None

if __name__ == '__main__':
    unittest.main()
