from api.v1.views import app_views
from models.tag import Tag
from flask import jsonify, make_response, request, abort
import models

@app_views.route("/tags", methods=["GET", "POST"], strict_slashes=False)
def all_tags():
    """
    GET - returns a list of all tag objects
    POST - creates a new tag
    """
    if request.method == "GET":
        all_tgs = models.storage.all("Tag").values()

        return make_response(jsonify([i.to_dict() for i in all_tgs]), 200)
    
    if request.method == "POST":
        data = request.get_json()

        if not data:
            abort(400, "Not a JSON")

        new = Tag(**data)
        new.save()

        return make_response(jsonify(new.to_dict()), 201)
    
@app_views.route("/tags/<tag_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def update_tag(tag_id):
    """
    GET - fetches a specific tag
    PUT - updates a tag
    DELETE - deletes a tag
    """

    tag = models.storage.get("Tag", str(tag_id))

    if tag is None:
        abort(404)

    if request.method == "GET":
        return make_response(jsonify(tag.to_dict()), 200)
    
    if request.method == "PUT":
        data = request.get_json()
        
        if data is None:
            abort(400, "Not a JSON")

        for i in data:
            if i not in ["id", "created_at", "update_at"]:
                setattr(tag, i, data[i])
        
        tag.save()
        return make_response(jsonify(tag.to_dict()), 200)
    
    if request.method == "DELETE":
        tag.delete()
        models.storage.save()
        return make_response(jsonify({}), 200)
    
@app_views.route("/search", methods=["Post"], strict_slashes=False)
def search():
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")