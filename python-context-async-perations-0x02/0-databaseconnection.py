import sqlite3

class DatabaseConnection:
    """
    A CM for handling database connections.
    """
    def __init__(self, db_name='airbnb.sqlite'):
        """
        Initialize the DB connection
        """
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """
        Open the DB connection
        """
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the DB connection
        """
        if self.connection:
            self.connection.close()
        return False

# test
def main():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)

if __name__ == "__main__":
    main()
