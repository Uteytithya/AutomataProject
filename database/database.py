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
    
    
