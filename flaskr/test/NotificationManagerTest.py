
# Import packages
import sqlite3;
import unittest;
from flaskr.databaseClasses.NotificationManager import DBNotification


class test_DBManager(unittest.TestCase):

    def setUp(self):
        self.con = sqlite3.connect("testdata/TestNotify.db");
        self.con.execute("PRAGMA foreign_keys = 1");
        self.cursor = self.con.cursor();
        self.cursor.execute("Insert into notification(userid,attributes) values(2,'TestGet')");
        self.cursor.execute("Insert into notification(userid,attributes) values(2,'TestGet2')");
        self.cursor.execute("Insert into notification(userid,attributes) values(1,'TestDelete')");
        self.cursor.execute("Insert into notification(userid,attributes) values(1,'TestNotify')");
        self.notify = DBNotification("testdata/TestNotify.db");
        self.con.commit();

    def test_a_AddNotify(self):
        self.notify.addNotify('1', 'TestAdd');
        result = self.con.execute("Select attributes From notification where attributes = 'TestAdd'");
        self.assertEqual(result.fetchall(),[('TestAdd',)]);

    def test_b_GetUsersNotifications(self):
        result = self.notify.getUsersNotifications('2');
        self.assertEqual(result,[(1,'TestGet'),(2,'TestGet2')]);
    
    def test_c_DeleteNotify(self):
        self.notify.deleteNotify('3');
        result = self.con.execute('Select attributes From notification where notifyid = 3');
        self.assertEqual(result.fetchall(),[]);
    
    def test_d_ModifyNotification(self):
        self.notify.modifyNotification(4,'Changed');
        result = self.con.execute("Select attributes From notification where attributes = 'Changed'");
        self.assertEqual(result.fetchall(),[('Changed',)]);
    
    def test_e_Cascade(self):
        self.con.execute("Insert into User(userid,email,password) values(9,'test','cascade')");
        self.con.execute("Insert into notification(userid,attributes) values(9,'atts')");
        self.con.execute("Delete From User Where userid = 9")
        result = self.con.execute('Select attributes From notification where userid = 9');
        self.assertEqual(result.fetchall(),[]);

    def tearDown(self):
        self.cursor.execute("Delete From notification");
        self.cursor.execute("Delete From User Where userid = 9");
        self.con.commit()
        self.con.close();

if __name__ == "__main__": 
    unittest.main()
