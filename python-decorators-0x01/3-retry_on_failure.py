import time
import sqlite3 
import functools

def with_db_connection(func):
    """
    A decorator that handles db connection lifecycle.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # connect
        connection = sqlite3.connect('users.db')
        try:
            return func(connection, *args, **kwargs)
        finally:
            connection.close()
    
    return wrapper

def retry_on_failure(retries=3, delay=2, backoff_factor=1.5, jitter=0.1):
    """
    Decorator to retry a function if it fails due to transient errors.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            
            while attempts <= retries:
                try:
                    return func(*args, **kwargs)
                
                except Exception as e:
                    attempts += 1
                    if attempts > retries:
                        raise
                    
                    print(f"Retry attempt {attempts}/{retries}. "
                          f"Waiting {delay} seconds. "
                          f"Error: {str(e)}")
                    
                    time.sleep(delay)
        
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

users = fetch_users_with_retry()
print(users)