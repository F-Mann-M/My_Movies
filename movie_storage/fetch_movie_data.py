import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def fetch_movie_data(title):
    """takes in movie title, trys to fetch the movie data from omdbapi and returns data"""
    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}={title}"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
