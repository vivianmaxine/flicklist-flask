from flask import Flask, request, redirect
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>FlickList</title>
    </head>
    <body>
        <h1>FlickList</h1>
"""

page_footer = """
    </body>
</html>
"""

# a form for adding new movies
add_form = """
    <style>
        .error {{
            color: red;
            font-weight: 800;
            font-family: Tahoma, Arial;
        }}
    </style>
    <form action="/add" method="post">
        <label>
            I want to add
            <input type="text" name="new-movie"/>
            to my watchlist.
        </label>
        <input type="submit" value="Add It"/>
        <p class="error">{new_movie_error}</p>
    </form>
    <br>
"""

def get_current_watchlist():
    # returns user's current watchlist--hard coded for now
    return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]

# a form for crossing off watched movies
# (first we build a dropdown from the current watchlist items)
crossoff_options = ""
for movie in get_current_watchlist():
    crossoff_options += '<option value="{0}">{0}</option>'.format(movie)

crossoff_form = """
    <form action="/crossoff" method="post">
        <label>
            I want to cross off
            <select name="crossed-off-movie"/>
                {0}
            </select>
            from my watchlist.
        </label>
        <input type="submit" value="Cross It Off"/>
    </form>
""".format(crossoff_options)

# a list of movies that nobody should have to watch
terrible_movies = [
    "Child's Play",
    "Child's Play 2",
    "Child's Play 3",
    "Bride of Chucky",
    "Seed of Chucky",
    "Curse of Chucky",
    "Cult of Chucky"
]


@app.route("/") # DISPLAYS THE FORMS
def index():
    edit_header = "<h2>Edit My Watchlist</h2>"

    # if we have an error, make a <p> to display it
    error = request.args.get("error")
    if error:
        error_esc = cgi.escape(error, quote=True)
        error_element = '<p class="error">' + error_esc + '</p>'
    else:
        error_element = ''

    # combine all the pieces to build the content of our response
    main_content = edit_header + add_form.format(new_movie_error='') + crossoff_form + error_element


    # build the response string
    content = page_header + main_content + page_footer

    return content

@app.route("/add", methods=['POST']) # PROCESSES ADD MOVIE FORM

# TODO 
# if the user typed nothing at all, redirect and tell them the error

def validate_movie():
    edit_header = "<h2>Edit My Watchlist</h2>"
    error_element = ''
    new_movie = request.form['new-movie']

    new_movie_error = ''
    error_message = None

    if new_movie == '':
        error_message = "Please enter a movie title."
    elif new_movie in terrible_movies:
        error_message = "Trust me, you don't want to add " + new_movie + " to your watchlist..."
    
    if error_message is not None:
        main_content = edit_header + add_form.format(new_movie_error=error_message, new_movie = '') + crossoff_form + error_element
        content = page_header + main_content + page_footer
        return content

    return redirect('/new_movie_success?new_movie={0}'.format(new_movie))
        
        
def add_movie():
    new_movie = request.form['new-movie']


    # TODO 
    # if the user wants to add a terrible movie, redirect and tell them not to add it b/c it sucks

    # build response content
    new_movie_element = "<strong>" + cgi.escape(new_movie) + "</strong>"
    sentence = cgi.escape(new_movie_element) + " has been added to your Watchlist!"
    content = page_header + "<p>" + sentence + "</p>" + page_footer

    return content

@app.route("/new_movie_success", methods=['GET'])
def valid_movie():
    new_movie = request.args.get('new_movie')
    return 'You have successfully added {0} to your watchlist.'.format(new_movie)

@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    if crossed_off_movie not in get_current_watchlist():
        # the user tried to cross off a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong
        error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

        # redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    # if we didn't redirect by now, then all is well
    crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
    confirmation = crossed_off_movie_element + " has been crossed off your Watchlist."
    content = page_header + "<p>" + confirmation + "</p>" + page_footer

    return content


app.run()
