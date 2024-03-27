#!/usr/bin/python3
"""
HANDLES DEFAULT RESTFUL API ACTIONS FOR RECIPES
"""
from models.recipe import Recipe
import models
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/recipes", methods=["GET"], strict_slashes=False)
def get_recipes():
    """
    RETRIEVES ALL RECIPE OBJECTS
    """
    all_recipes = models.storage.all("Recipe").values()
    result = []
    for item in all_recipes:
        result.append(item.to_dict())
    return make_response(jsonify(result))

@app_views.route("/recipes/<recipe_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_recipe(recipe_id):
    fetch = models.storage.get("Recipe", str(recipe_id))
    if fetch is None:
        abort(404)
    if request.method == "GET":
        return make_response(jsonify(fetch.to_dict()))