<<<<<<< HEAD
import mysql.connector as con
import mysql.connector.errors as Error
class database:
    def __init__(self):
            self.conn = con.connect(
                host="localhost",
                user="root",
                password="",
                database="automata",
                port = "3306"
            )

    def insertState(self, name):
        query = "INSERT INTO state (name) VALUES (%s)"
        cursor = self.conn.cursor()
        cursor.execute(query, (name,))
        self.conn.commit()
        cursor.close()
        print("State inserted successfully")
    
=======
class database:
    def __init__(self):
        pass
>>>>>>> 456b934c616ddd1be017a12bfde8e7e457c9e870
    def insertFA(self, Q, X, delta, q0, F, type, description):
        pass
    def getAllFA(self):
        pass
    def getFA(self, id):
        pass
    def deleteFA(self, id):
        pass
    def updateFA(self, id, Q, X, delta, q0, F, type, description):
        pass
    
<<<<<<< HEAD
db = database()
db.insertState("q1")
=======
    
>>>>>>> 456b934c616ddd1be017a12bfde8e7e457c9e870
