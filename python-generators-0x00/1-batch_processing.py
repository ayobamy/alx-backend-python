#!/usr/bin/python3

import mysql.connector
from typing import Dict, List, Generator

import seed

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict], None, None]:
    """
    Generator func to fetch users from the db
    
    Args:
        batch_size(int): No of users in each batch
    
    Return(Yields):
        List[Dict]: A batch of user dictionaries
    """
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        
        offset = 0
        
        while True:
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s", 
                (batch_size, offset)
            )
            
            batch = cursor.fetchall()
            
            if not batch:
                break
            
            yield batch
            
            offset += batch_size
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def batch_processing(batch_size: int) -> None:
    """
    Process users in batches
    
    Args:
        batch_size(int): No of users to process in each batch
    """
    for batch in stream_users_in_batches(batch_size):
        processed_users = [
            user for user in batch 
            if user['age'] > 25
        ]
        
        for user in processed_users:
            print(user)
