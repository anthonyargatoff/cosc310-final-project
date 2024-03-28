from ..distanceBetweenPoints.distanceBetweenPoints import coordinateCalculator
import unittest
import math

class test(unittest.TestCase):

    # Got hard-coded data from https://www.omnicalculator.com/other/latitude-longitude-distance

    def testGetDistanceKilometers(self):
        
        self.assertEqual(math.ceil(coordinateCalculator.getDistanceKilometers(61, 100, 60, 100)), 112)
        self.assertEqual(math.ceil(coordinateCalculator.getDistanceKilometers(9, 77, 4, 12)), 7195)
        self.assertEqual(math.ceil(coordinateCalculator.getDistanceKilometers(9, 77, 4, 12)), 7195)

    def testGetDistanceMiles(self):
        self.assertEqual(math.ceil(coordinateCalculator.getDistanceMiles(61, 100, 60, 100)), 70)
        
if __name__ == "__main__":
    unittest.main()
