from ..notification.Notification import Notification
import unittest

class test(unittest.TestCase):

    def setUp(self):
        # Setting up different edge cases
        self.t1 = Notification("magnitude:0-5.15;area:11.54,23.45,88.3;")
        self.t2 = Notification("magnitude:5.565-10;")
        self.t3 = Notification("magnitude:4.23-6.15;area:4.66,2.445,29.3;")
        self.t4 = Notification("area:50.54,-118.45,88.3;")

    # Tests the parsing and initialization
    def testInit(self):
        self.assertEqual(self.t1.minMagnitude, 0)
        self.assertEqual(self.t1.maxMagnitude, 5.15)
        self.assertEqual(self.t1.latitude, 11.54)
        self.assertEqual(self.t1.longitude, 23.45)
        self.assertEqual(self.t1.radius, 88.3)

        self.assertEqual(self.t2.minMagnitude, 5.565)
        self.assertEqual(self.t2.maxMagnitude, 10)
        self.assertEqual(self.t2.latitude, None)
        self.assertEqual(self.t2.longitude, None)
        self.assertEqual(self.t2.radius,None)

        self.assertEqual(self.t3.minMagnitude, 4.23)
        self.assertEqual(self.t3.maxMagnitude, 6.15)
        self.assertEqual(self.t3.latitude, 4.66)
        self.assertEqual(self.t3.longitude, 2.445)
        self.assertEqual(self.t3.radius, 29.3)

        self.assertEqual(self.t4.minMagnitude,None)
        self.assertEqual(self.t4.maxMagnitude, None)
        self.assertEqual(self.t4.latitude, 50.54)
        self.assertEqual(self.t4.longitude, -118.45)
        self.assertEqual(self.t4.radius, 88.3)

    def testIsMagnitudeSet(self):
        self.assertTrue(self.t1.isMagnitudeSet())
        self.assertTrue(self.t3.isMagnitudeSet())
        self.assertFalse(self.t4.isMagnitudeSet())

    def testIsDistanceSet(self):
        self.assertTrue(self.t1.isDistanceSet())
        self.assertFalse(self.t2.isDistanceSet())


    def testCompareMagnitude(self):
        self.assertTrue(self.t1.compareMagnitude(4))
        self.assertFalse(self.t1.compareMagnitude(8))

    def testCompareDistance(self):
        self.assertTrue(self.t1.compareDistance(11.44, 23.44))
        self.assertFalse(self.t1.compareDistance(12.44, 24.44))

    def testCompareNewEvent(self):
        self.assertTrue(self.t1.compareNewEvent(4.55, 11.44, 23.44))
        self.assertFalse(self.t1.compareNewEvent(4.55, 12.44, 24.44))
        self.assertTrue(self.t2.compareNewEvent(7, 44.55, 114.56))
        self.assertFalse(self.t2.compareNewEvent(3, 44.55, 112.44))
        self.assertTrue(self.t4.compareNewEvent(None, 50.5, -118.1))
        self.assertFalse(self.t4.compareNewEvent(None, 89.4, 4.1))


if __name__ == "__main__":
    unittest.main()

