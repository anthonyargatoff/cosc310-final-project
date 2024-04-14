
# Import package
import sqlite3
import unittest

from flaskr.databaseClasses import DBManager as DBM


class test_DBManager(unittest.TestCase):

    def setUp(self):
        self.con = sqlite3.connect("component_tests/testdata/TestUser.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("Insert into user(email,password) values('AAAA','BBBB')")
        self.cursor.execute("Insert into user(email,password) values('CCCC','DDDD')")
        self.cursor.execute("Insert into user(email,password,adminStatus) values('EEEE','FFFF',1)")
        self.con.commit()
        self.User = DBM.DBUser("component_tests/testdata/TestUser.db")
    
    def test_a_ValidateUser(self):
        self.assertTrue(self.User.validateUser('CCCC','DDDD'))
    
    def test_b_ValidateAdmin(self):
        self.assertTrue(self.User.validateAdmin('EEEE','FFFF'))

    def test_c_AddUser(self):
        self.User.addUser('Sample@test.com', 'BadPassword', 0)
        self.assertTrue(self.User.validateUser('Sample@test.com','BadPassword'))

    def test_d_DeleteUser(self):
        self.User.deleteUser('AAAA');
        result = self.cursor.execute("Select * From user Where email = 'AAAA'")
        self.assertEqual(result.fetchone(), None)
    
    def test_e_ModifyUser(self):
        self.User.modifyUser(1,'changed','alsochanged', 1)
        self.assertTrue(self.User.validateUser('changed','alsochanged'))
        self.User.modifyUser(1,'aaaaa','bbbbbb', 0)
    
    def test_f_SelectUserId(self):
        id = self.User.selectUserId('CCCC')
        self.assertEqual(id,3)

    def tearDown(self):
        self.cursor.execute("Delete From user Where email = 'Sample@test.com'")
        self.cursor.execute("Delete From user Where email = 'CCCC'")
        self.cursor.execute("Delete From user Where email = 'EEEE'")
        self.cursor.execute("Delete From user Where email = 'AAAA'")
        self.con.commit()
        self.con.close()

if __name__ == '__main__':
    unittest.main()

