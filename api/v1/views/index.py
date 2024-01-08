#!/usr/bin/python3
"""Start a Flask app"""
from flask import Flask, jsonify
from api.v1.views import app_views

"""Create an instance of Flask app"""
app = Flask(__name__)
@app.route("/status")
def status():
    """Returns with the status 'jsonified"""
    return jsonify({"status": "OK"})

@app.route("/api/v1/stats")
def endpoint():
    return 