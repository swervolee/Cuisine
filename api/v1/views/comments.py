from api.v1.views import app_views
from models.comment import Comment
from flask import make_response, jsonify, request, abort
import models

@app_views.route("/comments", methods=["GET"], strict_slashes=False)
def all_comments():
    '''
    Returns a list of all recipe comments
    '''
    comments = models.storage.get("Comment").values()