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
                filename='queries.log'
            )
            logger = logging.getLogger('database')
            
            query = kwargs.get('query') if 'query' in kwargs else args[0]
            
            logger.info(f"Executing query in {func.__name__}: {query}")
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error executing query: {str(e)}")
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

users = fetch_all_users(query="SELECT * FROM users")