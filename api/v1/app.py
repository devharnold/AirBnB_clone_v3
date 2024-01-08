#!/usr/bin/python3
""" Flask Application """
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import api_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Close the storage connection when the application context is torn down.

    This function is registered to be called automatically when the application
    context is about to be torn down, ensuring that the storage connection is
    properly closed. It helps with resource management and cleanup.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
