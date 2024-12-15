import sqlite3

class ExecuteQuery:
    """
    A CM for executing database queries with params
    """
    def __init__(self, db_name='airbnb.sqlite', query=None, params=None):
        """
        Initialize the query execution CM
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """
        Open DB connection and execute the query
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
        if self.query and self.params:
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
        
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the DB connection
        """
        if self.connection:
            self.connection.close()
        return False

# test
def main():
    with ExecuteQuery(query="SELECT * FROM users WHERE age > ?", params=(25,)) as results:
        if results:
            for row in results:
                print(row)

if __name__ == "__main__":
    main()