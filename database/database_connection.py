import sqlite3

class DatabaseConnection:
    def __init__(self, db_name="user_db.sqlite"):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection.cursor()

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, parameters=()):
        cursor = self.connect()
        cursor.execute(query, parameters)
        self.connection.commit()
        self.disconnect()
