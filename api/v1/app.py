#!/usr/bin/python3

from flask import Flask
import models
from api.v1.views import app_views
from os import getenv
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_apcontext(cmd):
    """
    CLOSES CURRENT STORAGE SESSION
    """
    models.storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    PAGE NOT FOUND HANDLER
    """
    return jsonify({"error": "Not found"}), 404



if __name__ == "__main__":
    host = getenv("CUISINE_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True, debug=True)
