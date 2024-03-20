#!/usr/bin/python3
from flask import Flask, render_template, url_for
from flask import request, redirect, sessions, flash
import flask_login
import models
from models.user import User
from models.recipe import Recipe
from models.tag import Tag
from models.comment import Comment
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv


app = Flask(__name__)
app.secret_key = b"eadff6d69ff0eb846bb982cb936f1bb20f48c091f04664378fd1c2de1769aa4c"
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
        if request.referrer:
            if request.referrer.split("/")[-1] == "login":
                return render_template("login.html", invalid=True)
        return render_template("login.html", invalid=False)

    elif request.method == "POST":
        submitted_email = request.form["email"]
        submitted_password = request.form["password"]
        remember_me = False

        user = next((u for u in users if u.email == submitted_email and u.password == submitted_password), None)

        if user is None:
            return redirect("login")

        if request.form["checkbox"] == "on":
            remember_me = True
        flask_login.login_user(user, remember=remember_me)
        sessions["user_id"] = user.id
        return redirect(url_for("cuisine"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    HANDLES USER SIGNUP
    """
    invalid_email = False
    existing_user = False

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        user = next((u for u in users if u.email == email), None)

        if user:
            existing_user = True
        else:
            try:
                valid = validate_email(email)
            except Exception as e:
                invalid_email = True
            else:
                send_login_email(email, "0.0.0.0:5000/cuisine")

    return render_template("signup.html",
                           existing=existing_user,
                           invalid_email=invalid_email)

def send_login_email(receiver_email, login_link):
    """
    VERIFIES EMAIL WHEN USER CREATES AN ACCOUNT
    """
    sender_email = "cuisinemailbox@gmail.com"
    password = getenv("EMAIL_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Login Authentication"

    body = f"""
    Hi,

    Here is your login authentication link:
    {login_link}

    Regards,
    Cuisine
    """

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
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
