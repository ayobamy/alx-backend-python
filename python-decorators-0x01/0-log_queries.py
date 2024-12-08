import sqlite3
import functools
import logging
from datetime import datetime

def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filename='database_queries.log'
            )
            query = kwargs.get('query', args[0] if args else None)
            if query:
                logging.info(f"Function: {func.__name__}")
                logging.info(f"Query: {query}")
                logging.info(f"Timestamp: {datetime.now()}")
            return func(*args, **kwargs)
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
