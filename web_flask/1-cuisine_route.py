#!/usr/bin/python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import EmailNotValidError, validate_email
from flask import Flask, flash, redirect, render_template, request, sessions, url_for
from flask_login import login_manager, current_user
from itsdangerous import URLSafeTimedSerializer
import flask_login
import models
import os
from os import getenv
import smtplib
from models.comment import Comment
from models.recipe import Recipe
from models.tag import Tag
from models.user import User
from quickstart import create_message, get_credentials, main, send_message
from werkzeug.utils import secure_filename

app = Flask(__name__)
SECRET_KEY = "eadff6d69ff0eb846bb982cb936f1bb20f48c091f04664378fd1c2de1769aa4c"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = "dp_uploads"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = models.storage.all("User").values()
login_tokens = []
serializer = URLSafeTimedSerializer(SECRET_KEY)

# --------------------------LOGIN----------------------------
@login_manager.user_loader
def user_loader(id):
    for i in models.storage.all("User").values():
        if i.id == id:
            return i
    return None

@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
@app.route("/login/<token>", strict_slashes=False)
def login(token=None):
    """
    HANDLES USER LOGIN
    """
    if request.method == "GET":
        if request.referrer:
            if request.referrer.split("/")[-1] == "login":
                return render_template("login.html", invalid=True)

        if token:
            try:
                unsealed = serializer.loads(token, max_age=300)
                new = User(**unsealed)
                new.save()
                print(unsealed)
            except Exception as e:
                print("Error in unsealing", e)
        return render_template("login.html", invalid=False)

    elif request.method == "POST":
        submitted_email = request.form["email"]
        submitted_password = request.form["password"]
        remember_me = False

        user = next((u for u in models.storage.all("User").values() if u.email == submitted_email and u.password == submitted_password), None)

        if user is None:
            return redirect("login")

        try:
            if request.form["checkbox"] == "on":
                remember_me = True
        except Exception:
            pass
        flask_login.login_user(user, remember=remember_me)
        return redirect(url_for("cuisine"))

@app.route("/signup", methods=["GET", "POST"], strict_slashes=False)
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

        user = next((u for u in models.storage.all("User").values() if u.email == email), None)

        if user:
            existing_user = True
        else:
            try:
                valid = validate_email(email)
            except Exception as e:
                invalid_email = True
            else:
                data = {"email": email,
                        "password": password,
                        "first_name": first_name,
                        "last_name": last_name,
                        }
                sealed = serializer.dumps(data)
                send_login_email(email, f"0.0.0.0:5000/login/{sealed}")
                return render_template("email-confirm.html")

    return render_template("signup.html",
                           existing=existing_user,
                           invalid_email=invalid_email)

def send_login_email(reciever, login_link):
    """
    VERIFIES EMAIL WHEN USER CREATES AN ACCOUNT
    """

    message = f"""
    Dear [User],

You are receiving this email because you requested to log in to your account on Cuisine. To proceed, please click on the link below:

{login_link}

This link will direct you to the login page where you can access your account securely. Please note that the link is valid for a limited time and will expire after 5 minutes.

If you did not request this login link or believe this email was sent to you in error, please disregard it and do not click on the link.

For security reasons, please do not share this login link with anyone. Additionally, ensure that you are accessing the login page from a secure and trusted device.

If you have any questions or need further assistance, please contact our support team at williamkubai101@gmail.com.

Thank you for choosing Cuisine.

Best regards,
Bree & William
Senior Devs
Cuisine
    """
    data = {"reciever": reciever,
            "subject": "Login Link for Cuisine",
            "message": message
            }

    main(**data)
#---------------------END OF LOGIN -------------------------------

#---------------------PROFILE UPLOAD------------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    """
    USER PROFILE PICTURE HANDLING
    """
    if 'profile_picture' not in request.files:
        return 'No file part'

    file = request.files['profile_picture']

    if file.filename == '':
        return 'No selected file'

    if file:
        # Generate a secure filename
        filename, extension = secure_filename(file.filename).split(".")

        identity = user_id()
        # Rename the file using the user id to make it have
        # a unique identity
        new_filename = identity + "_dp." + extension  # Specify the new filename

        # Save the file to the upload folder with the new filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        return 'File successfully uploaded as {}'.format(new_filename)

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
    return render_template("main.html", current_user=current_user)

@app.route("/about", strict_slashes=False)
def about():
    """
    THE ABOUT PAGE
    """
    return render_template("about.html")

@app.route("/status")
def status():
    """
    CHECK THE USER STATUS
    """
    if current_user.is_authenticated:
        return "Logged in"
    return "Anonymous"


@app.route("/user-creations", strict_slashes=False)
def user_creations():
    return render_template("user_creations.html")

def user_id():
    """
    RETURNS USER ID IF USER IS LOGGED IN
    """
    if current_user.is_authenticated:
        return current_user.id
    return None

if __name__ == "__main__":
    """
    MAIN FUNCTION
    """
    app.run(host="0.0.0.0", port=5000, debug=True)
