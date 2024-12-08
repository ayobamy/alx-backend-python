#!/usr/bin/python3

from mysql.connector import Error
import seed

def stream_user_ages():
    """
    Generator that yields user ages one by one from the db
    """
    conn = None
    cursor = None
    try:
        conn = seed.connect_to_prodev()
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
        if conn and conn.is_connected():
            conn.close()

def calculate_average_age():
    """
    Calculate average age
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        if age is not None:
            total_age += age
            count += 1
    
    if count == 0:
        return 0
        
    return total_age / count

def main():
    try:
        average_age = calculate_average_age()
        print(f"Average age of users: {average_age:.2f}")
            
    except Error as e:
        print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    main()
