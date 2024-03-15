#!/usr/bin/python3
"""
HANDLES DEFAULT RESTFUL API ACTIONS FOR RECIPES
"""
from models.recipe import Recipe
import models
from api.v1.view import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/recipes", methods=["GET"], strict_slashes=False)
def get_recipes():
    """
    RETRIEVES ALL RECIPE OBJECTS
    """
    all_states = models.storage.all("Recipe
