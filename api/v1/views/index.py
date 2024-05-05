#!/usr/bin/python3

"""
INDEX FILE
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    '''
    RETURNS SERVER STATUS
    '''
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=['GET'])
def stats():
    '''
    RETURNS OBJECT COUNT
    '''
    result = {
        'users': storage.count("User"),
        'recipes': storage.count("Recipe"),
        'tag': storage.count("Tag"),
        'comments': storage.count("Tag")
        }

    return jsonify(result)
