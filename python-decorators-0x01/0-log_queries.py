import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """
    Logs SQL queries before execution
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):   
        query = None
        if args and isinstance(args[0], str):
            query = args[0]
        elif 'query' in kwargs:
            query = kwargs['query']
            
        if query:
            print(f"\nFunction: {func.__name__}\nQuery: {query}\nTimestamp: {datetime.now()}\n{'='*50}")
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")