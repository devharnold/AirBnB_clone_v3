#!/usr/bin/python3

"""Start a Flask App
Import modules
"""
from flask import Flask, make_response, jsonify
from models import storage
import os
from api.v1.views import app_views

"""Create a variable instance of Flask"""
app = Flask(__name__)
app.register_blueprint(app)


@app.teardown_appcontext()
def teardown(exception):
    """Closes all the current storage session"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles Error message"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    threaded = os.environ.get('HBNB_API_THREADED', 'True').lower() == 'true'

    app.run(host=host, port=port, threaded=threaded, debug=True)