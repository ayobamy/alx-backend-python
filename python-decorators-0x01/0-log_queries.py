import sqlite3
import functools
import logging
from datetime import datetime

def log_queries():
    """
    Logs SQL queries before execution
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filename='database_queries.log'
            )
            
            query = None
            if args and isinstance(args[0], str):
                query = args[0]
            elif 'query' in kwargs:
                query = kwargs['query']
                
            if query:
                log_message = (
                    f"\nFunction: {func.__name__}\n"
                    f"Query: {query}\n"
                    f"Timestamp: {datetime.now()}\n"
                    f"{'='*50}"
                )
                logging.info(log_message)
            
            try:
                result = func(*args, **kwargs)
                return result
            except sqlite3.Error as e:
                logging.error(f"Database error in {func.__name__}: {str(e)}")
                raise
            except Exception as e:
                logging.error(f"Error in {func.__name__}: {str(e)}")
                raise
                
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")