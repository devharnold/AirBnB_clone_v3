#!/usr/bin/python3
"""int get methods"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status():
    """Returns with the status 'jsonified"""
    return jsonify({"status": "OK"})

@app_views.route("/api/v1/stats")
def stats():
    """
    Number of instances
    """
    return jsonify({
        "amenities": storage.count("Amenity"),
        "states": storage.count("State"),
        "reviews": storage.count("Review"),
        "users": storage.count("User"),
        "places": storage.count("Place"),
        "cities": storage.count("City")
    })