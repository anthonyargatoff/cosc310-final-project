
import sqlite3

class DBUser():

    def __init__(self, dbLocation):
        """Initialize a DBUser object for managing users in the database

        Args:
            dbLocation (String): file location of the database
        """
        self.dbLocation = dbLocation


    def addUser(self, email, password, adminstatus):
        """ Create a new tuple in user table with values email, password

        Args:
            email       (String):   email to be stored
            adminstatus (Integer):  whether new account should be an admin
            password    (String):   password to be stored.
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            con.execute("PRAGMA foreign_keys = 1")      # enforces foreign keys
            cursor = con.cursor();
            params = (email, password, adminstatus);
            SQL = "Insert Into user (email,password,adminStatus) values(?,?,?)"
            cursor.execute(SQL, params)
            con.commit()
            con.close()
        except Exception as e:
            print("Operation failed: ")
            print(e)
    
    def deleteUser(self, email):
        """ Delete user tuple based on email

        Args:
            email (String): email of user to be deleted.
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            con.execute("PRAGMA foreign_keys = 1")      # enforces foreign keys
            cursor = con.cursor()
            params = (email,)
            SQL = 'Delete From user Where email Like ?'
            cursor.execute(SQL,params)
            con.commit()
            con.close()
        except Exception as e:
            print("Operation failed: ")
            print(e)


    def modifyUser(self, id, newEmail, newPassword, adminstatus):
        """Modify user's email/password based on their userid, which must first be retrieved.
            if only one field needs modifying, just pass the other as it was retrieved from the database

        Args:
            id          (Integer):  User id, uniquely identifies user
            newEmail    (String):   new email address to be stored
            newPassword (String):   new password to be stored
            adminstatus (Integer):  new admin status (1 for admin, 0 for regular)
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            con.execute("PRAGMA foreign_keys = 1")      # enforces foreign keys
            cursor = con.cursor()
            params = (newEmail, newPassword, id, adminstatus)
            SQL = 'Update user Set email = ?, password = ?, adminStatus = ? Where userid = ? '
            cursor.execute(SQL,params)
            con.commit()
            con.close()
        except Exception as e:
            print("Operation failed: ")
            print(e)

    
    def validateUser(self, email,password):
        """Validate if email/password combo is found in DB. Also false on exception, so we can prompt user to try again.

        Args:
            email       (String): email associated with user
            password    (String): password associated with user

        Returns:
            Boolean: True if tuple found, else false
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            cursor = con.cursor()
            params = (email, password)
            SQL = 'Select email, password From user Where email = ? and password = ?'
            result = cursor.execute(SQL, params)
            list = result.fetchall()
            con.close()
            if (len(list)) != 1: 
                return False
            if (list[0][0] == email and list[0][1] == password):
                return True
            else: return False
        except Exception as e:
            print("Operation failed: ")
            print(e)
            return False

    def selectUserId(self, email):
        """ Select a users id by email(username)

        Args:
            email (String): Email of user to be selected

        Returns:
            List: userid associated with input email, false if email not found
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            cursor = con.cursor()
            params = (email,)
            SQL = "Select userid From user Where email = ?"
            result = cursor.execute(SQL,params)
            return result.fetchone()
        except Exception as e:
            print("Operation failed: ")
            print(e)
            return False

    def validateAdmin(self, email, password):
        """Validate if a given user account is an admin

        Args:
            email       (String): Email of account to check
            password    (String): Password of account to check

        Returns:
            boolean: True if account exists and is an admin, else false.
        """
        try:
            con = sqlite3.connect(self.dbLocation)
            cursor = con.cursor()
            params = (email, password)
            SQL = 'Select email, password, adminStatus From user Where email = ? and password = ?'
            result = cursor.execute(SQL, params)
            list = result.fetchall()
            con.close()
            if (len(list)) != 1: 
                return False
            if (list[0][0] == email and list[0][1] == password and list[0][2] == 1):
                return True
            else: return False
        except Exception as e:
            print("Operation failed: ")
            print(e)
            return False



