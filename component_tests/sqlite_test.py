# Import package
import sqlite3
import unittest

class test_SQLite(unittest.TestCase):

    # create connection and cursor
    def setUp(self):
        self.con = sqlite3.connect("component_tests/testdata/test.db")
        self.cursor = self.con.cursor()
        self.con.commit()

    #no test for just select, but all tests use select.

    # Test that pre-existing table still exists
    def test_Persistence(self):
        result = self.cursor.execute("Select * From T1")
        self.assertEqual(result.fetchall(),[(1, 'first'), (2, 'second')])

    # Test that creating tables works
    def test_Create(self):
        self.cursor.execute('Create Table testTable(id Integer)');
        result = self.cursor.execute("Select name From sqlite_master Where name='testTable'")
        self.assertEqual(result.fetchone(), ('testTable',))
        self.cursor.execute('Drop Table testTable')

    # Test that adding rows works
    def test_Insert(self):
        self.cursor.execute("Insert Into T1 values(5,'fifth'),(6,'sixth'),(7,'seventh')")
        result = self.cursor.execute("Select * From T1 Where id > 3")
        self.assertEqual(result.fetchall(), [(5, 'fifth'), (6, 'sixth'), (7, 'seventh')])
        self.cursor.execute("Delete From T1 Where id > 0")
    
    def tearDown(self):
        self.con.close()

if __name__ == '__main__':
    unittest.main()
