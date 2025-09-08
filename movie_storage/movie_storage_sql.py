from sqlalchemy import create_engine, text


# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL) #, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL
        )
    """))
    connection.commit()


def get_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


def add_movies(title, year, rating, poster):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"),
                               {"title": title, "year": year, "rating": rating, "poster": poster})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
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