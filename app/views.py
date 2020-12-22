import secrets
import random
import os
from app import app
from flask import render_template
from datetime import datetime
from flask import request, redirect, make_response, url_for, session
from pymongo import MongoClient

connect = "mongodb+srv://bkauyeung:241Engagement@engagement.pouvh.mongodb.net/engagement?retryWrites=true&w=majority"
client = MongoClient(connect)
db = client.engagement
# Just make it so that you require a name, no Password
# The name becomes a session id and a seed.
# Then we redirect them to the picture template.

app.config["SECRET_KEY"] = 'JlKNQEhzCaANybR1eA0n'


login = {"dana": "dana7k@berkeley.edu", "bryan": "password", "casey":"casey.king@yale.edu", "vasanth":"rlvasanth@berkeley.edu", "alexandra":"saveale@berkeley.edu", "test":"test"}
# number = {"dana": 0, "bryan": 0, "casey":0, "vasanth":0, "alexandra":0, "test":0}

@app.route("/sign-up-cookie-example", methods=["GET", "POST"])
def sign_up_cookie_example():

    if request.method == "POST":

        req = request.form

        username = req.get("username")
        password = req.get("password")

        if username not in login:
            feedback = "Please enter a valid name."
            return render_template("public/sign_up_example_cookie.html", feedback=feedback)


        if password != login[username]:
            feedback = "Wrong password."
            return render_template("public/sign_up_example_cookie.html", feedback=feedback)

        session["USERNAME"] = username
        # session['picture_index'] = 0 # NOTE: This does not persist between computers!
        # Look up the index in the metadata collection
        session['picture_index'] = db.metadata.find()[0][username]
        print("The session username is set.")

        return redirect(url_for("picture"))
    return render_template("public/sign_up_example_cookie.html")


@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/picture", methods=["GET", "POST"])
def picture():
    if "USERNAME" in session:  # Existing user
        username = session.get("USERNAME")
        seed = username # For clarity
        picture_index = int(session['picture_index'])
        # return render_template("public/dynamic_cookie.html", user=user)

        photo_files = os.listdir('app/static/img/photos')
        photo_files = [file for file in photo_files]

        # FOR JUST BRYAN DANA AND Vasanth
        # sorted(photo_files, key = lambda student: int(student[7:-4]))
        #
        # if username == 'vasanth':
        #     photo_files = photo_files[:200]
        #
        # if username == 'dana':
        #     photo_files = photo_files[:50]+photo_files[201:350]
        #
        # if username == 'bryan':
        #     photo_files = photo_files[:50]+photo_files[351:500]

        # Set the seed for randomizing pictures. Use your own instance of random so you dont create a
        # race condition.
        r = random.Random(seed)
        r.shuffle(photo_files)

        # r = random.Random(seed)
        # r.shuffle(photo_files)
        # Show the next photo by index.
        if picture_index < 1095:
            sample_pic = 'img/photos/' + photo_files[picture_index]

        else:
            return redirect(url_for("completed_grading"))

        if request.method == "POST":
            req = request.form

            answer1 = req.get("behavior")
            answer2 = req.get("emotional")

            pic_data = {
            'user_id':username,
            'picture' : photo_files[picture_index],
            'behavior' : answer1,
            'emotion' : answer2
            }

            # Stores the information into the database.
            # Collection name is pictures.
            db.pictures.insert_one(pic_data)
            # Increase the index by 1
            session["picture_index"]+=1
            return redirect(request.url)

        return render_template("public/picture.html", sample_pic=sample_pic, picture_number=picture_index+1)

    else:
        print("No username found in session")
        return redirect(url_for("sign_up_cookie_example"))


@app.route("/completed-grading")
def completed_grading():
    # session.pop("USERNAME", None)
    return render_template("public/finish.html")


@app.route("/sign-out")
def sign_out():
    username = session.get("USERNAME")
    myquery = {}
    new_values = {"$set": {username: session['picture_index']}}
    db.metadata.update_one(myquery, new_values)
    # picture_index = int(session['picture_index'])
    # number[username]=picture_index
    session.pop("USERNAME", None)
    return redirect(url_for("index"))

#####################################################################################################
####### Bryan's Practice code (nothing to do with engagement) is below

@app.route("/cookie_profile")
def cookie_profile():
    # This is where the server takes information from the cookie on the client side.
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = users[username]
        return render_template("public/dynamic_cookie.html", user=user)
    else:
        print("No username found in session")
        return redirect(url_for("sign_up_cookie_example"))

@app.route("/about")
def about():
    return """
    <h1 style='color: red;'>I'm a red H1 heading!</h1>
    <p>This is a lovely little paragraph</p>
    <code>Flask is <em>awesome</em></code>
    """

    return render_template("public/sign_up.html")

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form
        print(req)

        username = req.get("username")
        email = req["email"]
        password = request.form["password"]

        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/sign_up.html", feedback=feedback)

        return redirect(request.url)
    return render_template("public/sign_up.html")


@app.route("/cookies")
def cookies():
    resp = make_response("Set cookies")
    # resp.set_cookie("flavor", value="chocolate chip", max_age=10, path=request.path)

    cookies = request.cookies
    print(cookies)

    resp.set_cookie("chocolate type", "dark")
    resp.set_cookie("chewy", "yes")
    # flavor = cookies.get("flavor")
    return resp

@app.route("/jinja")
def jinja():

    # Strings
    my_name = "Bryan"

    # Integers
    my_age = 28

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
            "Troyo": 39,
            "Gustavo": 15,
            "Pedro": 29,
            "Shawno":26,
            "Potato":28
    }

    # Tuples
    colors = ("Red", "Blue")


    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def pull(self):
            return f"Pulling repo '{self.name}'"
        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name = "Learning Flask",
        description = "Learn the Flask web framework for Python",
        domain = "https://github.com/Bryan-Auyeung/learning-flask.git"
    )

    # Functions
    def repeat(x, qty=1):
        return x*qty

    date = datetime.utcnow()


    return render_template("public/jinja.html", my_name=my_name, my_age=my_age, langs=langs, friends=friends, colors=colors, cool=cool, GitRemote=GitRemote, my_remote=my_remote, repeat=repeat, date=clean_date(date))



@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/profile/<username>")
def profile(username):
    user = None

    users = {
        "mitsuhiko": {
            "name": "Armin Ronacher",
            "bio": "Creatof of the Flask framework",
            "twitter_handle": "@mitsuhiko"
        },
        "gvanrossum": {
            "name": "Guido Van Rossum",
            "bio": "Creator of the Python programming language",
            "twitter_handle": "@gvanrossum"
        },
        "elonmusk": {
            "name": "Elon Musk",
            "bio": "technology entrepreneur, investor, and engineer",
            "twitter_handle": "@elonmusk"
        }
    }

    if username in users:
        user = users[username]
    return render_template("public/dynamic.html", username=username, user=user)

users = {
    "julian": {
        "username": "julian",
        "email": "julian@gmail.com",
        "password": "example",
        "bio": "Some guy from the internet",
        "seed": 101,
        "ind":0
    },
    "clarissa": {
        "username": "clarissa",
        "email": "clarissa@icloud.com",
        "password": "sweetpotato22",
        "bio": "Sweet potato is life",
        "seed": 111,
        "ind":0
    },
    "alexandra": {
        "username": "alexandra",
        "password": "apple",
        "bio": "I like red dresses",
        "seed": 123,
        "ind":0,
    }
}
