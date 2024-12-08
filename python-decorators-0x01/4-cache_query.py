import time
import json
import sqlite3 
import functools


query_cache = {}

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

def cache_query(func):
    """
    A decorator that caches db query results.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        cache_key = (query, json.dumps(args), json.dumps(kwargs))
        
        if cache_key in query_cache:
            print(f"Cached query: {query} with parameters")
            return query_cache[cache_key]
        
        result = func(conn, query, *args, **kwargs)
        
        query_cache[cache_key] = result
        print(f"Caching result for query: {query}")
        
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")