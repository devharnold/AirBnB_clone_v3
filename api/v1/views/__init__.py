#!/usr/bin/python3
"""Start a Flask app
    Import all models used

"""
from flask import Flask, Blueprint
from api.v1.views import app_states
from api.v1.views import app_cities
from api.v1.views import app_amenities
from api.v1.views import app_places
from api.v1.views import app_users
from api.v1.views import placesreviews

"""Import Blueprints from files"""
from .states import states_bp
from .cities import city_bp
from .amenities import amenity_bp
from .places_reviews import placesreviews_bp
from .users import users_bp
from .places import places_bp

"""Register app_views blueprint"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""Register respective blueprints"""
cities.register_blueprint(city_bp)
amenities.register_blueprint(amenity_bp)
states.register_blueprint(states_bp)
placesreviews.register_blueprint(placesreviews_bp)
users.register_blueprint(users_bp)
places.register_blueprint(places_bp)
