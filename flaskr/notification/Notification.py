from flaskr.distanceBetweenPoints.distanceBetweenPoints import coordinateCalculator

class Notification:
    """
    Determines whether or not a notification should be sent to a user
    """
    def __init__(self, dbAttributes: str):
        """
        Initialization automatically parses input.

        Args:
            dbAttributes (str): Attributes string from the database in format : magnitude:3-6;area:14,35,44; -- area is lat, lon, radius
        """        

        # Define all the variables, then check if they exist
        self.minMagnitude = None
        self.maxMagnitude = None
        self.latitude = None
        self.longitude = None
        self.radius = None
        
        # parse the string with ; as deliminator
        splitString = dbAttributes.split(";")

        for element in splitString:
            #check if magnitude exists, and then assigns it 
            if "magnitude" in element:
                magnitudeSplit = element.split(":")
                magnitudeRange = magnitudeSplit[1].split("-")
                self.minMagnitude, self.maxMagnitude = float(magnitudeRange[0]), float(magnitudeRange[1])

            # check if area exists
            if "area" in element:
                areaSplit = element.split(":")
                location = areaSplit[1].split(",")
                self.latitude, self.longitude, self.radius = float(location[0]), float(location[1]), float(location[2])

    def isMagnitudeSet(self)->bool:
        """
        Determines if a user has set a notification for magnitude.

        Returns:
            bool: Returns true if a magnitude is set.
        """        
        return (self.maxMagnitude is not None and self.minMagnitude is not None)
    
    def isDistanceSet(self)->bool:
        """
        Determines if a user has set a notification for area. 

        Returns:
            bool: Returns true if an area has been set.
        """        
        return (self.latitude is not None and self.longitude != None and self.radius is not None)
    
    def compareMagnitude(self, magnitude:float)->bool:
        """
        Compares user's notification setting of magnitude to the new incoming data

        Args:
            magnitude (float): A float value for magnitude size

        Returns:
            bool: Returns true if the user's setting matches argument
        """           
        return (magnitude > self.minMagnitude and magnitude < self.maxMagnitude)

    def compareDistance(self, latitude:float, longitude:float)->bool:
        """
        Compares user's notification setting of area to the new incoming data

        Args:
            latitude (float): Float of latitude
            longitude (float): float of longitude

        Returns:
            bool: Returns true if the user's setting matches the argument
        """        
        return (coordinateCalculator.getDistanceKilometers(self.latitude, self.longitude, latitude, longitude) <= self.radius)

    def compareNewEvent(self, magnitude:float, latitude:float, longitude:float) -> bool:
        """
        Given arguments of magnitude, latitude, and longitude, this method will return true if all parameters are met

        Args:
            magnitude (float): Float of magnitude size
            latitude (float): Float of latitude
            longitude (float): Float of longitude

        Returns:
            bool: Returns true if all parameters are met
        """
        if (self.isMagnitudeSet() and not self.isDistanceSet()):
            if(magnitude):
                return self.compareMagnitude(magnitude)
            else:
                return False
        
        elif (not self.isMagnitudeSet() and self.isDistanceSet()):
            if (latitude and longitude):
                return self.compareDistance(latitude, longitude)
            else:
                return False

        elif (self.isDistanceSet() and self.isDistanceSet()):

            magnitudeBool = False
            distanceBool = False

            if (magnitude):
                magnitudeBool = self.compareMagnitude(magnitude)

            if (latitude and longitude):
                distanceBool = self.compareDistance(latitude, longitude)

            return (magnitudeBool and distanceBool)
        
        else:
            return False

        
        
        
    