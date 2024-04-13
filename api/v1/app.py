#!usr/bin/python3


from flask import Flask, request, jsonify, current_app
import models
from api.v1.views import app_views
from os import getenv
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
def after_request(response):
  # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5001')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response



@app.teardown_appcontext
def teardown_apcontext(cmd):
    """
    CLOSES CURRENT STORAGE SESSION
    """
    models.storage.save()
    models.storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    PAGE NOT FOUND HANDLER
    """
    return jsonify({"Error 404": "Not Found"}), 404

if __name__ == "__main__":
    host = getenv("CUISINE_API_HOST", "0.0.0.0")
    port = int(getenv("CUISINE_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True, debug=True)
