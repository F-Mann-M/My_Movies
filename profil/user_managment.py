from sqlalchemy import create_engine, text
from profil.current_user import set_current_user, get_current_user

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL) #, echo=True)

# Create user table
with engine.connect() as connection:
    query = "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)"
    connection.execute(text(query))
    connection.commit()


def add_user(user_name):
    """prompts user to input username, adds user to SQLite user database"""
    # Get username
    query = "INSERT INTO users (name) VALUES (:name) RETURNING user_id"
    params = {"name": user_name}

    # Add username
    with engine.connect() as connection:
        try:
            result = connection.execute(text(query), params)
            user_id = result.scalar()
            connection.commit()
            print(f"User '{user_name}' successfully added to users.")
            set_current_user(user_id, user_name)
        except Exception as e:
            print(f"Error: {e}")
            return


def get_user_list():
    """Retrieve all movies from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT user_id, name FROM users"))
            users_list = result.fetchall()

        return {row[0]: {"name": row[1]} for row in users_list}
    except Exception as e:
        print(f"Error: {e}")


def delete_user():
    """delete user form database"""
    user_id, user_name = get_current_user()
    query_user = "DELETE FROM users WHERE user_id = :user_id"
    query_user_movie = "DELETE FROM user_movie WHERE user_id = :user_id"
    params = {"user_id": user_id}
    try:
        with engine.connect() as connection:
            connection.execute(text(query_user), params)
            connection.execute(text(query_user_movie), params)
            connection.commit()
            set_current_user(None, None)
            print(f"User '{user_name}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")

