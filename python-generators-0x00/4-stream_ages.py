#!/usr/bin/python3

from mysql.connector import Error
import seed

def stream_user_ages(conn):
    """
    Generator that yields user ages one by one from the db
    """
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT age FROM user_data")
        
        for row in cursor:
            yield float(row['age'])
            
    except Error as e:
        print(f"Error fetching ages: {e}")
        yield None
    finally:
        if cursor:
            cursor.close()

def calculate_average_age(conn):
    """
    Calculate average age
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages(conn):
        if age is not None:
            total_age += age
            count += 1
    
    if count == 0:
        return 0
        
    return total_age / count

def main():
    conn = None
    try:
        conn = seed.connect_to_prodev()
        if conn:
            average_age = calculate_average_age(conn)
            print(f"Average age of users: {average_age:.2f}")
            
    except Error as e:
        print(f"Error connecting to database: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
