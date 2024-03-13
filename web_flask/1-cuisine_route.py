#!/usr/bin/python3
from flask import Flask, render_template
import models
from models.user import User
from models.recipe import Recipe
from models.tag import Tag
from models.comment import Comment
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """
    CLOSES THE CURRENT SQLALCHEMY SESSION
    """
    models.storage.close()

@app.route("/cuisine", strict_slashes=False)
def cuisine():
    """
    CUISINE WEBFLASK
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

    return render_template("0-index.html",
                           recipes=recipes,
                           comments=comments,
                           tags=tags)

if __name__ == "__main__":
    """
    MAIN FUNCTION
    """
    app.run(host="0.0.0.0", port=5000, debug=True)
