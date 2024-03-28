import unittest
import json
from  flaskr.earthquakeAPI.EarthquakeApi import EarthquakeApi
import os

testFileLocation = 'flaskr/test/testdata/'

class test_Api(unittest.TestCase):

    def setUp(self):
         self.e = EarthquakeApi('https://earthquake.usgs.gov/fdsnws/event/1/')

    def test_getAllJSONData(self):

        self.e.getAllDataJSON("1568-01", "1568-01", testFileLocation)

        with open(testFileLocation + "getAllDataTest.json", "r") as f1:
            data1 = json.load(f1)
        
        with open(testFileLocation + "1568_01.json", "r") as f2:
            data2 = json.load(f2)

        self.assertEqual(data1["features"][0]["id"], data2["features"][0]["id"])
        os.remove(testFileLocation + "1568_01.json")
       

    def test_getParsedDataJSON(self):
        self.e.getParsedDataJSON("1568-01", "1568-01", testFileLocation)

        with open(testFileLocation + "getParsedDataTest.json", "r") as f:
            data1 = json.load(f)
        with open(testFileLocation + "getParsedDataTest.json", "r") as f:
            data2 = json.load(f)
        
        self.assertEqual(data1[0]["title"], data2[0]["title"])
        os.remove(testFileLocation + "earthquakesParsed.json")


    def test_getParsedDataTXT(self):
        self.e.getParsedDataTXT("1568-01", "1568-01", testFileLocation, False)

        with open(testFileLocation + "getParsedDataTest.txt") as f:
            data1 = f.read()
        with open(testFileLocation + "1568-01_to_1568-01.txt") as f:
            data2 = f.read()

        self.assertEqual(data1, data2)
        os.remove(testFileLocation + "1568-01_to_1568-01.txt")


    def test_getLast24Hours(self):
        self.assertTrue(self.e.getLast24Hours())

if __name__ == '__main__':
    unittest.main()