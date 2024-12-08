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

def transactional(func):
    """
    Decorator to manage database transactions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn')
        if conn is None:
            raise ValueError("No database connection provided. Use with @with_db_connection.")
        
        try:
            conn.execute('BEGIN')
            result = func(*args, **kwargs)
            conn.commit()

            return result
        except Exception as e:
            conn.rollback()
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')