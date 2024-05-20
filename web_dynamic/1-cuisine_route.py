#!/usr/bin/python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import EmailNotValidError, validate_email
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask import make_response, jsonify
from flask_cors import CORS
from flask_login import LoginManager, current_user
from itsdangerous import URLSafeTimedSerializer
import flask_login
import models
import os
import uuid
from os import getenv
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
cache_id = str(uuid.uuid4())
CORS(app, resources={r"/*": {"origins": "*"}})





# --------------------------LOGIN----------------------------


@app.route("/logout", methods=["POST"], strict_slashes=False)
def logout():
    """
    AN API TO LOGOUT USER

    This function logs out the user by calling the `flask_login.logout_user()` function.
    It then renders the "main.html" template with the `current_user` and `cache_id` variables.

    Returns:
        The rendered template "main.html" with the `current_user` and `cache_id` variables.
    """
    flask_login.logout_user()
    return render_template("main.html", current_user=current_user, cache_id=cache_id)

@login_manager.user_loader
def user_loader(id):
    """
    Load a user from the database based on the given ID.

    Args:
        id (int): The ID of the user to load.

    Returns:
        User: The user object if found, None otherwise.
    """
    for i in models.storage.all("User").values():
        if i.id == id:
            return i
    return None

@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
@app.route("/login/<token>", strict_slashes=False)
def login(token=None):
    """
    Handles user login.

    Args:
        token (str, optional): A token for user authentication. Defaults to None.

    Returns:
        str: The rendered login template or a redirect to the cuisine route.

    Raises:
        Exception: If there is an error in unsealing the token.

    """
    if request.method == "GET":
        if request.referrer:
            if request.referrer.split("/")[-1] == "login":
                return render_template("login.html", invalid=True, cache_id=cache_id)

        if token:
            try:
                unsealed = serializer.loads(token, max_age=300)
                new = User(**unsealed)
                new.save()
                print(unsealed)
                current_user.is_authenticated = True
            except Exception as e:
                print("Error in unsealing", e)
        current_user.is_authenticated = True
        return render_template("login.html", invalid=False, cache_id=cache_id)

    elif request.method == "POST":
        submitted_email = request.form["email"]
        submitted_password = request.form["password"]
        remember_me = True

        user = None
        for i in models.storage.all("User").values():
            if i.email == submitted_email and i.password == submitted_password:
                user = i

        if user is None:
            return redirect(url_for("login"))
        try:
            if request.form["checkbox"] == "on":
                remember_me = True
        except Exception:
            pass
        flask_login.login_user(user, remember=True)
        return redirect(url_for("cuisine"))

@app.route("/signup", methods=["GET", "POST"], strict_slashes=False)
def signup():
    """
    HANDLES USER SIGNUP

    This function handles the user signup process. It receives a POST request with user information
    such as email, password, first name, last name, and confirm password. It validates the input data,
    checks if the email is already registered, and sends a confirmation email to the user if the data is valid.

    Returns:
        If the request method is POST and the data is valid, it renders the "email-confirm.html" template.
        If the request method is GET or the data is invalid, it renders the "signup.html" template with appropriate
        error messages.
    """
    invalid_email = False
    existing_user = False

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        confirm_password = request.form["confirm_password"]

        if confirm_password != password:
            return render_template("signup.html", password_mismatch=True, cache_id=cache_id)

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
                send_login_email(email, f"https://web-02.monadoll.tech/login/{sealed}")
                return render_template("email-confirm.html", cache_id=cache_id)

    return render_template("signup.html",
                           existing=existing_user,
                           invalid_email=invalid_email,
                           cache_id=cache_id)

def send_login_email(reciever, login_link):
    """
    VERIFIES EMAIL WHEN USER CREATES AN ACCOUNT
    """

    message = f"""
    Dear User,

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

    return render_template("recipe.html", recipes=recipes, comments=comments, tags=tags, user_id=user_id, cache_id=cache_id)


@app.route("/", strict_slashes=False)
def cuisine():
    """
    LANDING PAGE FOR CUISINE
    """
    # path = "web_dynamic/static/images/display_images/"
    # fnames = []
    # for filename in os.listdir(path):
    #    fnames.append("../static/images/display_images/" + filename)
    return render_template("main.html", current_user=current_user, cache_id=cache_id)

@app.route("/about", strict_slashes=False)
def about():
    """
    THE ABOUT PAGE
    """
    return render_template("about.html", cache_id=cache_id)


@app.route("/user-creations", strict_slashes=False)
def user_creations():
    """
    Renders the user creations page with the user's recipes, comments, and tags.

    Returns:
        The rendered user_creations.html template with the following variables:
        - recipes: A list of the user's recipes.
        - comments: A list of the user's comments.
        - cache_id: The cache ID.
        - tags: A list of all tags.
    """
    fetch_id = user_id()
    if id:
        user = models.storage.get("User", fetch_id)
        if user:
            recipes = [r for r in user.recipes]
            comments = [c for c in user.comments]
            tags = models.storage.all("Tag").values()
        
            return render_template("user_creations.html", recipes=recipes, comments=comments, cache_id=cache_id, tags=tags)
    return render_template("user_creations.html", cache_id=cache_id)

@app.route("/recipe_creation", methods=["GET"], strict_slashes=False)
def recipe_creation():
    """
    Renders the recipe_creation.html template with the cache_id parameter.

    Returns:
        The rendered template with the cache_id parameter.
    """
    return render_template("recipe_creation.html", cache_id=cache_id)

def user_id():
    """
    Returns the user ID if the user is logged in.

    Returns:
        int or None: The user ID if the user is logged in, None otherwise.
    """
    if current_user.is_authenticated:
        return current_user.id
    return None

@app.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Returns the status of the user.

    If the user is authenticated, it returns a JSON response with the status "logged" and the user's ID.
    If the user is not authenticated, it returns a JSON response with the status "anonymous".

    Returns:
        A JSON response with the user's status.
    """
    if current_user.is_authenticated:
        data = {"status": "logged",
                "id": current_user.id}
        return make_response(jsonify(data), 200)
    
    else:
        return make_response(jsonify({"status": "anonymous"}))

if __name__ == "__main__":
    """
    MAIN FUNCTION
    """
    app.run(host="0.0.0.0", port=5001, debug=False)
