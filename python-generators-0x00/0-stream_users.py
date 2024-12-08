import mysql.connector
import seed

def stream_users():
    """
    streams rows from an SQL database one by one
    
    Return: user rows from streaming db
    """
    try:
        connection = seed.connect_to_prodev()
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        for user in cursor:
            yield user
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    
    finally:
        if cursor:
            try:
                cursor.fetchall()
            except mysql.connector.Error:
                pass
            cursor.close()
        
        if connection:
            connection.close()