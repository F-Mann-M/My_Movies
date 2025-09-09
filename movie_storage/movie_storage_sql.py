from sqlalchemy import create_engine, text

from profil.current_user import get_current_user


# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL) #, echo=True)

# Query to create movies table if it does not exist
query_add_movies_table = "CREATE TABLE IF NOT EXISTS movies ( id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE NOT NULL, year INTEGER NOT NULL, rating REAL NOT NULL, poster TEXT NOT NULL )"
# Query to create the user_movie table if it does not exist
query_add_user_movie_table = ("CREATE TABLE IF NOT EXISTS user_movie (user_id INTEGER NOT NULL, movie_id INTEGER NOT NULL)")
# Query to create the users tabel
query_add_user_table = "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)"

with engine.connect() as connection:
    # create movies table
    connection.execute(text(query_add_movies_table))
    # create user_movies table
    connection.execute(text(query_add_user_movie_table))
    # create users table
    connection.commit()


def get_movies():
    """Retrieve all movies from the database."""
    user_id, user_name = get_current_user()
    query = f"""SELECT title, rating, year, poster FROM movies JOIN user_movie ON movies.id = user_movie.movie_id WHERE user_movie.user_id = :user_id"""
    params = {"user_id": user_id}
    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


def add_movies(title, year, rating, poster):
    """
    Add a new movie to the movies table if it does not exit
    get the id of the new row add it along with user id to user_movie table
    """
    user_id, user_name = get_current_user()
    params = {"title": title, "year": year, "rating": rating, "poster": poster, "user_id": user_id}
    query_add_movie = "INSERT OR IGNORE INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster);"
    query_get_movie_id = "SELECT id FROM movies WHERE title = :title"
    query_link_user_to_movie = "INSERT INTO user_movie (user_id, movie_id) VALUES (:user_id, :movie_id)"
    with engine.connect() as connection:
        try:
            connection.execute(text(query_add_movie), params)
            result = connection.execute(text(query_get_movie_id), params)
            movie_id = result.scalar()
            connection.execute(text(query_link_user_to_movie), {"movie_id": movie_id, "user_id": user_id})
            connection.commit()
            print(f"Movie '{title}' added successfully with database.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    query = "DELETE FROM movies WHERE title = :title"
    params = {"title": title}
    try:
        with engine.connect() as connection:
            connection.execute(text(query), params)
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")

    except Exception as e:
        print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    query = "UPDATE movies SET rating = :rating WHERE title = :title"
    params = {"title": title, "rating": rating}
    try:
        with engine.connect() as connection:
            connection.execute(text(query), params)
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
