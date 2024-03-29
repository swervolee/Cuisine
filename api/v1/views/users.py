from api.v1.views import app_views
from models.user import User
from flask import abort, make_response, jsonify, request
import models

@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def users():
    """
    GET - Returns a list of all user objects
    POST - Creates a new user

    If an invalid json is provided for post method return 400 status code
    """
    if request.method == "GET":
        users = models.storage.all("User").values()
        return make_response(jsonify([i.to_dict() for i in users]), 200)
    elif request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "first_name" not in data:
            abort(400, "Missing first name")
        elif "last_name" not in data:
            abort(400, "Missing last_name")
        elif "email" not in data:
            abort(400, "Missing Email")
        elif "password" not in data:
            abort(400, "Missing Password")
        new = User(**data)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)

@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def update_user(user_id):
    """
    GET - Returns user with the specific id
    PUT - Updates a user object's attributes
    DELETE - Deletes a user instance

    If no instance of the id is found, returns 404 status code
    If an invalid or non-json is given for PUT method returns 400 status code
    """
    user = models.storage.get("User", str(user_id))
    if user is None:
        abort(404)
    if request.method == "GET":
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for i in data:
            if i not in ["created_at", "updated_at", "id"]:
                setattr(user, i, data[i])
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == "DELETE":
        user.delete()
        models.storage.save()
        return make_response(jsonify({}), 200)