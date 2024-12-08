import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that handles db connection lifecycle.
    
    Args:
        func: The function requiring a database connection
        
    Returns:
        wrapper: The wrapped function with automatic connection handling
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

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

user = get_user_by_id(user_id=1)
print(f"Retrieved user: {user}")