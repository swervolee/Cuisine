from api.v1.views import app_views
from models.comment import Comment
from flask import make_response, jsonify, request, abort
import models

@app_views.route("/comments", methods=["GET"], strict_slashes=False)
def all_comments():
    '''
    Returns a list of all recipe comments
    '''
    comments = models.storage.all("Comment").values()
    return make_response([i.to_dict() for i in comments], 200)

@app_views.route("/users/<user_id>/comments", methods=["GET", "POST"])
def user_comments(user_id):
    user = models.storage.get("User", user_id)

    if user is None:
        abort(404)
    
    if request.method == "GET":
        result = user.comments
        return make_response(jsonify([i.to_dict() for i in result]), 200)
    
    if request.method == "POST":
        data = request.get_json()

        if data is None:
            abort(404)
        
        if "message" not in data:
            abort(400, "Missing message")
        if "recipe_id" not in data:
            abort(400, "Missing recipe_id")
        
        recipe = models.storage.get("Recipe", data["recipe_id"])

        if recipe is None:
            abort(404)