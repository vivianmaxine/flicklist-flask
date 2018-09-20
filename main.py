import random
from flask import Flask

#FlickList 1

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

@app.route("/")
def index():
    # choose a movie by invoking our new function
    movie_today = get_random_movie()
    movie_tomorrow = get_random_movie()

    # build the response string
    content = "<h1>Movie of the Day</h1>"
    content += "<ul>"
    content += "<li>" + movie_today + "</li>"
    content += "</ul>"

    # TODO: pick another random movie, and display it under
    # the heading "<h1>Tommorrow's Movie</h1>"

    content += "<h1>Tomorrow's Movie</h1>"
    content += "<ul>"
    content += "<li>" + movie_tomorrow + "</li>"
    content += "</ul>"

    return content

def get_random_movie():
    movie_list = ["Crazy Rich Asians", "Acrimony", "Prime", "500 Days of Summer", "Uncle Buck"]
    # TODO: randomly choose one of the movies, and return it
    random_movie = movie_list[random.randint(0,len(movie_list) - 1)]
    return random_movie


app.run()
