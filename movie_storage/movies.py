#Title: My Movie App
#Version: 1.0 (first iteration)


import statistics, random
import matplotlib.pyplot as plt
from movie_storage.movie_storage_sql import add_movies, get_movies, update_movie, delete_movie
from movie_storage.fetch_movie_data import fetch_movie_data
from movie_storage.page_generator import generate_page
from profil.user_managment import get_user_list, add_user, delete_user
from profil.current_user import set_current_user, get_current_user


def get_movie_list():
    """loads a dictionary and prints all movies along with their rating and year of release."""
    user_id, user_name = get_current_user()
    print(f"\n==========={user_name}'s movie list===========")

    # get movies
    movies = get_movies()
    if movies is None:
        print("Your movie list is empty")
        return None

    #print movies in total
    print(f"{len(movies)} movies in total")

    # print all the movies along with their rating and year of release
    for movie in movies:
        title = movie
        rating = movies.get(movie)["rating"]
        year = movies.get(movie)["year"]
        print(f"Title: {title}\n"
            f"Rating: {rating}\n"
            f"Year of release: {year}\n")


def add_movie():
    """
    loads a dictionary of dictionaries and gets 3 inputs (title, rating, year) from user
    and adds a new title along with rating and year to the dictionary if not already in dictionary.
    """
    print("\n===========Add movie===========")

    # get movies
    movies = get_movies()
    if movies is None:
        return None

    # prompt user to enter movie and rating. If movie is not in dictionary add new title and rating to dict
    while True:
        title = input("New movie name: ")
        if not title:
            print("Invalid input!")
            continue
        elif title in movies:
            print(f"Movie {title} already exist!")
            continue


        # fetch movie data
        movie_data = fetch_movie_data(title)
        if movie_data is not None and movie_data:
            movie_title = movie_data.get("Title")
            year = movie_data.get("Year")
            rating = movie_data.get("imdbRating")
            poster = movie_data.get("Poster")

            #add movies to database
            if movie_title:
                add_movies(movie_title, year, rating, poster)
            else:
                print(movie_data.get("Error"))

        return None


def comment_delete_movie():
    """Takes in a list of dictionaries and ask user for title
    if the title is in dictionary it will be deleted
    """
    print("\n===========Delete movie===========")
    movies = get_movies()
    if movies is None:
        return None

    title = input("Which movie do you want to delete: ")
    if not title:
        print("Invalid input!")
        return None
    elif title not in movies:
        print(f"Movie {title} not exist!")
        return None
    else:
        delete_movie(title)
        #print(f"Movie {title} was successfully removed!")
    return None


def comment_update_movie():
    """loads a dictionary, asks user for title and rating, updates title if in dictionary"""
    print("\n===========Update list===========")
    movies = get_movies()
    if movies is None:
        return None

    title = input("Which movie do you want to update? ")
    if title in movies:
        rating = check_rating_input("Enter new rating: ", None)
        if rating is None:
            return None
        update_movie(title, rating)
        print(f"{title} was successfully updated")
        return None
    else:
        print(f"Movie {title} not found!")
    return None


def get_movie_stats():
    """loads a dictionary,
    calculates and prints:
    - average rating
    - median rating
    - best rating
    - worst rating
    """
    print("\n===========Stats===========")

    movies = get_movies() # load movies
    if movies is None:
        return None

    movies_rating = []
    highest_rating = 0
    best_movies = []
    lowest_rating = 10  # start with the highest rating possible
    worst_movies = []

    #get list of ratings
    for movie in movies:
        title = movie
        rating = movies.get(movie)["rating"]

        movies_rating.append(rating) # to calculate the average and median rating

        # get movie(s) with highest rating
        if rating > highest_rating:
            highest_rating = rating
            best_movies = [(title, rating)]
        elif rating == highest_rating: # check if there is another movie with equal rating
            best_movies.append((title, rating))

        # get worst movie(s) with rating
        if rating < lowest_rating:
            lowest_rating = rating
            worst_movies = [(title, rating)]
        elif rating == lowest_rating: # check if there is another movie with equal rating
            worst_movies.append((title, rating))

    #calculate and print average rating in the database
    average = sum(movies_rating) / len(movies) #sum ratings (values) and divide them by length
    print(f"Average rating: {round(average, 2)}")

    #calculate and print median rating by using statistics.median()
    median = statistics.median(movies_rating)
    print(f"Median rating: {median}")

    #print best movie(s) along with rating
    for movie, rating in best_movies:
        print(f"Best movie: {movie}: {rating}")

    # print worst movie(s) along with rating
    for movie, rating in worst_movies:
        print(f"Worst movie: {movie}: {rating}")

    print("\n")


def print_random_movie():
    """Takes in a dictionary and prints a random key with value by using modul random"""
    print("\n===========Random movie===========")
    movies = get_movies()
    if movies is None:
        return None

    random_movie, info = random.choice(list(movies.items())) #choose a random movie form list
    print(f"Movie: {random_movie}\n"
          f"Rating: {info["rating"]}\n"
          f"Year of release: {info["year"]}")


def search_movie():
    """Takes in a dictionary and user input. Checks if input is in dictionary"""
    print("\n===========Search movie===========")
    movies = get_movies()
    if movies is None:
        return None

    user_input = input("Enter part of movie name: ")
    if not user_input:
        print("Invalid input!")
        return None
    for movie in movies:
        title = movie
        rating = movies.get(movie)["rating"]
        year = movies.get(movie)["year"]
        if user_input.casefold() in title.casefold():
            print(f"Movie: {title}\n"
                  f"Rating: {rating}\n"
                  f"Year of release: {year}")
    return None


def movies_sorted_by_rating():
    """Takes in a dictionary and prints all the movies and their ratings in descending order by the rating."""
    print("\n===========Movies sorted===========")
    movies = get_movies()
    if (movies is
            None):
        return None

    movies_list = [(title, info) for title, info in movies.items()]
    movies_sorted = sorted(movies_list, key=lambda info: info[1]["rating"], reverse = True)
    for index in range(len(movies_sorted)):
        title = movies_sorted[index][0]
        rating = movies_sorted[index][1]["rating"]
        year = movies_sorted[index][1]["year"]
        print(f"Movie: {title}\nRating: {rating}\nYear of release: {year}\n")


def show_histogram():
    """Takes in a dictionary. Uses values of dictionary to create histogram by using library matplotlib.pyplot"""
    print("\n===========Histogram===========")
    movies = get_movies()
    if movies is None:
        return None

    ratings = []
    for movie, info in movies.items():
        ratings.append(info["rating"])  #get ratings and store in list "ratings"
    plt.hist(ratings)               #creates plot/histogram
    plt.show()                      #Displays the plot


def show_movies_chronological():
    movies = get_movies()
    if movies is None:
        return None

    user_choice = input("Do you want the latest movies first? (Y/N) ")
    is_reverse = False
    if user_choice.lower() == "y":
        is_reverse = True
    elif user_choice.lower() == "n":
        is_reverse = False
    movies_list = [(title, info) for title, info in movies.items()]
    movies_sorted = sorted(movies_list, key = lambda item: item[1]["year"], reverse = is_reverse)
    for index in range(len(movies_sorted)):
        title = movies_sorted[index][0]
        rating = movies_sorted[index][1]["rating"]
        year = movies_sorted[index][1]["year"]
        print(f"Movie: {title}\nRating: {rating}\nYear of release: {year}\n")


def check_rating_input(prompt, default_value):
    """
    takes in str (prompt) and float (default).
    Asks for users input. If input is empty return default value
    otherwise checks if user_input is a number between 0 and 10
    and return user_input as float.
    Else print Error
    """
    while True:
        user_input = input(prompt)
        if not user_input and default_value is not None: #if default None do not return default value
            return float(default_value)
        try:
            value = float(user_input)
            if 0 <= value <= 10:
                return value
            else:
                print("Invalid input! Rating must be a float between 0 and 10")
        except ValueError:
            print("Invalid rating! Enter a number!")


def check_year_input(prompt, default_value):
    """
    Takes in a prompt (str) and integer (default_value)
    prompt user to enter a value
    checks if input is not empty. If empty return default value as int
    checks if input are digits and return as float
    otherwise print error
    """
    while True:
        user_input = input(prompt)
        if not user_input and default_value is not None:
            return int(default_value)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Invalid input! Enter a valid year")


def filter_movies():
    print("\n===========Filter Movies===========")
    movies = get_movies()
    if movies is None:
        return None

    rating = check_rating_input("Enter minimum rating (leave blank for no minimum rating): ", 0)
    if rating is None:
        return None
    start_year = check_year_input("Enter start year (leave blank for no end year): ", 0)
    if start_year is None:
        return None
    end_year = check_year_input("Enter end year (leave blank for no end year): ", 9999)
    if end_year is None:
        return None
    print(f"rating {rating}, start_year: {start_year}, end_year: {end_year}")

    # print filtered movies
    for title, info in movies.items():
        if info["rating"] >= rating and start_year <= info["year"] <= end_year:
            print(f"Movie: {title}\nRating: {info["rating"]}\nYear of release: {info["year"]}\n")
    return None


def exit_program():
    print("Bye!")
    exit()


def command_add_user():
    """prompt user to input username, checks if username is not in list and valid, add name to users database"""
    user_list = get_user_list()
    users = [user_name["name"] for user_id, user_name in user_list.items()]

    while True:
        new_user = input("Enter username: ")
        if new_user in users:
            print(f"User {new_user} already exist")
        elif not new_user:
            print("Invalid input")
        else:
            add_user(new_user)
            movies()


def select_user():
    """shows a list of user with id. prompt user to choos a user by id. calls movie app"""
    users = get_user_list()
    user_id, user_name = get_current_user()
    print("\n========Select User=========\n")
    if user_name is not None:
        print(f"Enter 'del' to delete current user: {user_name}")
    print("Enter 'add' to add new user")
    print("\nOr select a user by number: ")
    for user_id, user in users.items():
        print(f"{user_id}. {user["name"]}")

    while True:
        try:
            selected_user_id = input("Enter a number: ")

            if selected_user_id == "add":
                command_add_user()
                return None
            elif selected_user_id == "del":
                delete_user()
                select_user() #reload to update list of users
            elif selected_user_id:
                set_current_user(int(selected_user_id), users[int(selected_user_id)].get("name"))
                movies()
        except Exception as e:
            print(f"Error: {e}")


def movies():
    """Prints the menu, gets the input of the user and calls function depending on the user input."""
    user_id, user_name = get_current_user()
    print(f"\n\nWelcome back, {user_name}! 🎬")

    while True:
        # print menu
        print(f'''\n********** {user_name}'s Movie Database **********
Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Histogram
10. Movies sorted by year
11. Filter movies
12. Generate website
13. switch user
        ''')

        # dispatch table of functions
        menu_dict = {
            "0": exit_program,
            "1": get_movie_list,
            "2": add_movie,
            "3": comment_delete_movie,
            "4": comment_update_movie,
            "5": get_movie_stats,
            "6": print_random_movie,
            "7": search_movie,
            "8": movies_sorted_by_rating,
            "9": show_histogram,
            "10": show_movies_chronological,
            "11": filter_movies,
            "12": generate_page,
            "13": select_user
        }


        # get user choice
        user_choice = input("Enter choice (1-13): ")

        # call function
        if user_choice in menu_dict:
            menu_dict[user_choice]()
        else:
            print("invalid input")

        input("\nPress enter to continue ")

