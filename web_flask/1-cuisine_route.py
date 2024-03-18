#!/usr/bin/python3
from flask import Flask, render_template, url_for, request, redirect, sessions, flash
import flask_login
import models
from models.user import User
from models.recipe import Recipe
from models.tag import Tag
from models.comment import Comment

app = Flask(__name__)
app.secret_key = "eadff6d69ff0eb846bb982cb936f1bb20f48c091f04664378fd1c2de1769aa4c"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = models.storage.all("User").values()

# --------------------------LOGIN----------------------------
@login_manager.user_loader
def user_loader(id):
    for i in users:
        if i.id == id:
            return i

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    HANDLES USER LOGIN
    """
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        submitted_email = request.form["email"]
        submitted_password = request.form["password"]

        user = next((u for u in users if u.email == submitted_email and u.password == submitted_password), None)

        if user is None:
            return redirect(url_for("login"))

        flask_login.login_user(user)
        return redirect(url_for("cuisine"))

@app.route("/signup")
def signup():
    """
    HANDLES USER SIGNUP
    """
    if request.method == "GET":
        return render_template("signup.html")
    else:
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        user = next((u for u in users if u.email == email and u.password == password), None)

        if user:
            flash("An account with this email already exists. Please sign in or use a different email.", "error")

#---------------------END OF LOGIN -------------------------------


@app.teardown_appcontext
def close_db(error):
    """
    CLOSES THE CURRENT SQLALCHEMY SESSION
    """
    models.storage.close()


@app.route("/recipes", strict_slashes=False)
def cuisine_recipes():
    """
    PRESENTS AVAILABLE RECIPES
    """
    recipes = [r for r in models.storage.all("Recipe").
               values() if r.private == False]
    recipes = sorted(recipes, key=lambda k: k.title)

    for item in recipes:
        item.instructions = item.instructions.strip("\n")
        item.Instructions = item.instructions.split("\n")

        item.ingredients = item.ingredients.strip("\n")
        item.Ingredients = item.ingredients.split("\n")

    comments = models.storage.all("Comment").values()

    for item in comments:
        item.user = models.storage.get("User", item.user_id);

    tags = models.storage.all("Tag").values()

    return "hello"


@app.route("/", strict_slashes=False)
def cuisine():
    """
    LANDING PAGE FOR CUISINE
    """
    return render_template("main.html")

@app.route("/about", strict_slashes=False)
def about():
    """
    THE ABOUT PAGE
    """
    return render_template("about.html")


@app.route("/user-creations", strict_slashes=False)
def user_creations():
    return "hellow world"

if __name__ == "__main__":
    """
    MAIN FUNCTION
    """
    app.run(host="0.0.0.0", port=5000, debug=True)
