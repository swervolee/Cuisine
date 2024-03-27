from api.v1.views import app_views
from models.user import User
from flask import abort, make_response, jsonify
import models

@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    users = models.storage.all("User").values()
    return make_response(jsonify([i.to_dict() for i in users]), 200)