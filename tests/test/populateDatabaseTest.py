import os
import sqlite3;
import unittest;
from flaskr.databaseClasses.populateDatabase import populateDb

testDb = os.path.abspath("flaskr/test/testdata/test.db")
testLocation = "flaskr/test/testdata/"

class Test(unittest.TestCase):

    def setUp(self):
        self.con = sqlite3.connect(testDb)
        self.cursor = self.con.cursor()

    # Test the populateDatabase.py adding from text file works as expected
    def test_InsertFromTextFile(self):
        self.cursor.execute('CREATE TABLE earthquakesTest (id INTEGER PRIMARY KEY AUTOINCREMENT,title VARCHAR(50),eventTime datetime,magnitude decimal (6, 4),latitude decimal (9, 6),longitude decimal (9, 6), depth decimal (10,6), url varchar(255));')
        x = populateDb(testDb, testLocation + 'multipleLinesTest.txt')
        x.populateAllTxtData("earthquakesTest")
        result = self.cursor.execute("SELECT latitude FROM earthquakesTest WHERE id=4")
        self.assertEqual(result.fetchall(), [(40.059,)])
        self.cursor.execute("DROP TABLE earthquakesTest;")

    def tearDown(self):
        self.con.close()

if __name__ == '__main__':
    unittest.main()