from movie_storage.movie_storage_sql import get_movies


def load_html_template(file_path):
    """loads html template"""
    with open(file_path, "r") as file:
        return file.read()


def generate_html_content_from_movies():
    """takes in movie data from sqlite database and return html code as string"""
    movies = get_movies()
    new_string = ""

    for movie in movies:
        title = movie
        poster = movies.get(movie)["poster"]
        year = movies.get(movie)["year"]
        new_string += f"""<li>
            <div class="movie">
                <img class="movie-poster" src="{poster}">
                <div class="movie-title">{title}</div>
                <div class="movie-year">{year}</div>
            </div>
        </li>"""
    return new_string


def write_html(new_html):
    """loads html as string and saves it as index.html"""
    with open ("./static/index.html", "w") as file:
        file.write(new_html)

    print("Website was successfully generated to the file animals.html.")


def generate_page():
    """loads html template, replaces old string with new string, returns a html"""
    html_temp = load_html_template("./static/index_template.html")
    html_new = html_temp.replace("__TEMPLATE_TITLE__", "My Movie App")
    old_string = "__TEMPLATE_MOVIE_GRID__"
    new_string = generate_html_content_from_movies()
    new_html = html_new.replace(old_string, new_string)
    write_html(new_html)