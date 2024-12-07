import csv
import uuid
import mysql.connector
from mysql.connector import Error


def connect_db():
    """
    Connect to MySQL server.
    
    Returns:
        Db connection object
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='ahmed',
            password='donola4real'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """
    Create the ALX_prodev database if NOT EXISTS.
    
    Args:
        connection: Db connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()

def connect_to_prodev():
    """
    Connect to ALX_prodev database.
    
    Returns:
        Db connection object
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='ahmed',
            password='donola4real',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None
    

def create_table(connection):
    """
    Create the user_data table if NOT EXISTS.
    
    Args:
        connection: Db connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            UNIQUE INDEX idx_email (email)
        )
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()


def insert_data(connection, data):
    """
    Insert data into the user_data table.
    
    Args:
        connection: Db connection object
        csv_file (str): Path to the CSV file
    """
    try:
        cursor = connection.cursor()
        
        # SQL query to insert data
        query = """
        INSERT IGNORE INTO user_data (user_id, name, email, age) 
        VALUES (%s, %s, %s, %s)
        """
        
        with open(data, 'r') as csvfile:
            next(csvfile)
            csv_reader = csv.reader(csvfile)
            
            records = [
                (str(uuid.uuid4()), row[0], row[1], float(row[2])) 
                for row in csv_reader
            ]
        
        cursor.executemany(query, records)
        connection.commit()
        
        print(f"Inserted {cursor.rowcount} records successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"Error: CSV file {data} not found")
    finally:
        if cursor:
            cursor.close()
