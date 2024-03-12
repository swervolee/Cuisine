#!/usr/bin/python3
from flask import Flask
import models
from models.user import User
from models.recipe import Recipe
from models.tag import Tag
from models.comment import Comment
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def cuisine_root():
    """
    APPLICATION ROOT
    """
    return "Hi there, welcome to cuisine"

@app.route("/cuisine", methods=["GET"], strict_slashes=False)
def cuisine():
    """
    PRINTS CUISINE
    """
    return "Cuisine"

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
