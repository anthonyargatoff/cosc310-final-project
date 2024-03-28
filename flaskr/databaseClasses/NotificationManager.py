import sqlite3

class DBNotification():
    """
    Manages notifications stored in the Database
    """

    def __init__(self, dbLocation):
        self.dbLocation = dbLocation

    """
    Initialize the class.

    Args:
        dbLocation (string): File location for the database.
    """
    
    def addNotify(self, userid, settings):
        """
        Adds a notification to the database.

        Args:
            userid      (String):   Id of user setting notification
            settings    (String):   String encoding magnitude settings ('>5', '<8', '=3', etc.)
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            con.execute("PRAGMA foreign_keys = 1")      # enforces foreign keys
            cursor = con.cursor();
            params = (userid, settings)
            SQL = "Insert Into notification(userid, attributes) values(?,?)"
            cursor.execute(SQL, params)
            con.commit()
            con.close()
        except Exception as e:
            print("transaction failed: ")
            print(e)


    def getUsersNotifications(self, userid):
        """
        Returns a list of the Users notifications, (notifyid, attributes).

        Args:
            userid      (String):   Id of user whose notifications are being requested
        """
        
        try:
            con = sqlite3.connect(self.dbLocation)
            cursor = con.cursor()
            params = (userid,)
            SQL = "Select notifyid, attributes From notification Where userid = ?"
            result = cursor.execute(SQL, params)
            return result.fetchall()
        except Exception as e:
            print("transaction failed: ")
            print(e)


    def deleteNotify(self, notifyid):
        """
        deletes a notification from the database.

        Args:
            notifyid    (String):   Id of notification to be deleted
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            con.execute("PRAGMA foreign_keys = 1")      # enforces foreign keys
            cursor = con.cursor()
            params = (notifyid,)
            SQL = "Delete From notification Where notifyid = ?"
            cursor.execute(SQL, params)
            con.commit()
            con.close()
        except Exception as e:
            print("transaction failed: ")
            print(e)

    def modifyNotification(self, notifyid, newAttributes):
        """
        modify a notification from the database based on its notifyid. Can't change the user associated with the notification.

        Args:
            notifyid    (String):   Id of notification to be deleted
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            con.execute("PRAGMA foreign_keys = 1");      # enforces foreign keys
            cursor = con.cursor();
            params = (newAttributes, notifyid)
            SQL = 'Update notification Set attributes = ? Where notifyid = ? '
            cursor.execute(SQL,params)
            con.commit()
            con.close()
        except Exception as e:
            print("transaction failed: ")
            print(e)

