import sqlite3

class SqlConnection:
    def __init__(self, database_file):
        self.database_file = database_file
        self.connection = self.connect_to_database()

    def connect_to_database(self):
        try:
            connection = sqlite3.connect(self.database_file)
            print("Connected to the database")
            self.create_user_credentials_table(connection)
            return connection
        except sqlite3.Error as err:
            print(f"Error: {err}")
            return None

    def create_user_credentials_table(self, connection):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS user_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        '''
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database")

    def insert_user_credentials(self, username, password):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                insert_query = "INSERT INTO user_credentials (username, password) VALUES (?, ?)"
                cursor.execute(insert_query, (username, password))
                self.connection.commit()
                cursor.close()
                print("User credentials inserted successfully")
            else:
                print("Database connection is not established")
        except sqlite3.Error as err:
            print(f"Error: {err}")



    def create_expense_table(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                name TEXT,
                amount TEXT,
                month TEXT
            );
        '''
        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def insert_expense(self, date, name, amount, month):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                insert_query = "INSERT INTO expenses (date, name, amount, month) VALUES (?, ?, ?, ?)"
                cursor.execute(insert_query, (date, name, amount, month))
                self.connection.commit()
                cursor.close()
                print("Expense inserted successfully")
            else:
                print("Database connection is not established")
        except sqlite3.Error as err:
            print(f"Error: {err}")

    def get_expenses_by_month(self, month):
        cursor = self.connection.cursor()
        cursor.execute("SELECT date, name, amount FROM expenses WHERE month = ?", (month,))
        results = cursor.fetchall()
        cursor.close()
        return results
