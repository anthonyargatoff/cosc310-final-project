import unittest
from flaskr.distanceBetweenPoints.prediction import predictionCalculator

class test_Prediction(unittest.TestCase):

    def setUp(self):
        self.testdata = [{'latitude': 61.6795, 'longitude': -143.2598}, {'latitude': -5.2583, 'longitude': 134.2234}, 
                         {'latitude': -28.9513, 'longitude': -176.3111}, {'latitude': 60.6494, 'longitude': -151.4802}, 
                         {'latitude': 59.8559, 'longitude': -150.5184}, {'latitude': 32.9043333, 'longitude': -115.5225}, 
                         {'latitude': 11.6018, 'longitude': 57.6959}, {'latitude': 67.7689, 'longitude': -157.4438}, 
                         {'latitude': 33.477, 'longitude': -116.5283333}, {'latitude': 61.1781, 'longitude': -146.7708}, 
                         {'latitude': 38.7961655, 'longitude': -122.7426682}, {'latitude': -42.8557, 'longitude': -16.0022}, 
                         {'latitude': 59.8906, 'longitude': -139.4907}, {'latitude': 32.901, 'longitude': -115.5228333}, 
                         {'latitude': 44.6095, 'longitude': -112.9396667}, {'latitude': 38.7668343, 'longitude': -122.7109985}];
        
        self.expected = [{'count': 2, 'latitude': 32.9043333, 'longitude': -115.5225},
                           {'count': 2, 'latitude': 38.7961655, 'longitude': -122.7426682},
                           {'count': 1, 'latitude': 61.6795, 'longitude': -143.2598},
                           {'count': 1, 'latitude': -5.2583, 'longitude': 134.2234},
                           {'count': 1, 'latitude': -28.9513, 'longitude': -176.3111},
                           {'count': 1, 'latitude': 60.6494, 'longitude': -151.4802},
                           {'count': 1, 'latitude': 59.8559, 'longitude': -150.5184},
                           {'count': 1, 'latitude': 11.6018, 'longitude': 57.6959},
                           {'count': 1, 'latitude': 67.7689, 'longitude': -157.4438},
                           {'count': 1, 'latitude': 33.477, 'longitude': -116.5283333}];

    def testGetPredictions(self):
        preds = predictionCalculator.getPredictions(self.testdata);
        self.assertEqual(preds,self.expected)

    def tearDown(self):
        print();

unittest.main();
