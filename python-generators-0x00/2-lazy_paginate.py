#!/usr/bin/python3

import seed


def paginate_users(page_size, offset):
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    finally:
        connection.close()

def lazy_pagination(page_size):
    """
    Generator function to lazily paginate users from the database.
    
    Args:
        page_size(int): No of users to fetch in each page
    
    Yields:
        list: A page of user records
    """
    offset = 0
    
    while True:
        page = paginate_users(page_size, offset)
        
        if not page:
            break
        yield page
        
        offset += page_size
