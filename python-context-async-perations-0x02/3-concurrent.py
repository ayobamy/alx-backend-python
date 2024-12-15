import asyncio
import aiosqlite

async def async_fetch_users():
    """
    Fetch all users
    """
    async with aiosqlite.connect('airbnb.sqlite') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """
    Fetch users older than 40
    """
    async with aiosqlite.connect('airbnb.sqlite') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """
    Execute both async DB queries concurrently
    """
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("---------------------------\nAll the Users:\n---------------------------")
    for user in users:
        print(user)
    print("\n")
    print("---------------------------\nUsers Older Than 40:\n---------------------------")
    for user in older_users:
        print(user)

def main():
    asyncio.run(fetch_concurrently())

if __name__ == "__main__":
    main()
