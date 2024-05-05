#!/usr/bin/python3
"""
HANDLES DEFAULT RESTFUL API ACTIONS FOR RECIPES
"""
from models.recipe import Recipe
from models.user import User
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
    """
    GET - Returns a single recipe object with id provided
    PUT - Updates a recipe instance's attributes
    DELETE - Deletes  a recipe instance of id provided

    If no instance is found of given id, returns 404 status code
    If invalid json is given, return 400 status code
    """
    fetch = models.storage.get("Recipe", str(recipe_id))
    if fetch is None:
        abort(404)
    if request.method == "GET":
        return make_response(jsonify(fetch.to_dict()))
    elif request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        else:
            for key in data:
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(fetch, key, data[key])
                fetch.save()
        return make_response(jsonify(fetch.to_dict()), 200)
    elif request.method == "DELETE":
        fetch.delete()
        models.storage.save()
        return make_response(jsonify({})), 200
@app_views.route("users/<user_id>/recipes", methods=["GET", "POST"], strict_slashes=False)
def create_recipe(user_id):
    """
    CREATES A RECIPE OBJECT

    GET - An alternative way to get a recipe but through a user id
    POST - A recipe must have a creator. Creates a recipe with the given user id as the creator

    Args:
        user_id (str): The ID of the user creating the recipe

    Returns:
        Response: The HTTP response containing the created recipe in JSON format

    Raises:
        404: If the user with the given user_id does not exist
        400: If the request data is not in JSON format

    """
    usr = models.storage.get("User", str(user_id))
    if usr is None:
        abort(404)
    if request.method == "GET":
        return make_response(jsonify([i.to_dict() for i in usr.recipes]), 200)
    
    if request.method == "POST":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        new = Recipe(**data)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)
    

@app_views.route("users/<user_id>/recipes/favorites/", methods=["GET", "POST", "DELETE"], strict_slashes=False)
def user_favorites(user_id):
    """
    Retrieve, add, or remove favorite recipes for a specific user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        A response containing the favorite recipes in JSON format.

    Raises:
        404: If the user with the specified ID does not exist.
        400: If the request is not in JSON format or if the recipe ID is missing.
    """
    user = models.storage.get("User", user_id)
    if user is None:
        abort(404)
    
    if request.method == "GET":
        result = user.favorites
        return make_response(jsonify([i.to_dict() for i in result]), 200)
    
    if request.method == "POST" or request.method == "DELETE":
        data = request.get_json()

        if data is None:
            abort(400, "Not a JSON")
        if "recipe_id" not in data:
            abort(400, "Missing recipe_id")
        
        recipe = models.storage.get("Recipe", data["recipe_id"])

        if recipe is None:
            abort(404)
        if request.method == "POST":
            user.favorites = recipe
        elif request.method == "DELETE":
            user.unfavorite(recipe)
        models.storage.save()
        info = {f"{user_id}_favorites": [i.to_dict() for i in user.favorites]}
        
        if request.method == "POST":
            return make_response(jsonify(info), 201)
        else:
            return(make_response(jsonify(info)), 200)