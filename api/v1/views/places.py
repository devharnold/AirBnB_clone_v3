#!/usr/bin/python3

"""
Import Various Modules
"""
from flask import Blueprint, make_response, jsonify, abort, request
from models import Place
from api.v1.views import app_views

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """Get the places by city"""
    city = Place.query.get(city_id)
    if city is None:
        abort(404)
    
    places = Place.query.filter(city_id=city_id).all()
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)

@app_views.route('/places/<place_id>', methods=['GET'])
def get_placeobj(place_id):
    """Get places by object"""
    place = Place.query.get(place_id)
    if place_id is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete Places"""
    place = Place.query.get(place_id)
    if place_id is None:
        abort(404)
    place.delete()
    return jsonify({})

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create Place
    Transform HTTP request toa dictionary
    If HTTP request body not valid JSON, raise 400 error
    """
    city = next((c for c in city if c['id'] == city_id), None)
    if city is None:
        abort(404, description='City not found')
    
    if not request.is_json:
        abort(404, description='Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description='Missing user_id')

    if 'user_id' is None:
        abort(404)
    
    data = request.get_json()
    if 'name' not in data:
        abort(400, description='Missing name')

    new_place = {
        'name': data['name'],
        'city_id': city_id
    }
    return jsonify(new_place), 201

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update place
    Transform HTTP request to a dictionary
    Update Place with all key-value pairs of the dictionary
    """
    place = Place.query.get(place_id)
    if place is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            raise ValueError("Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'user_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    except ValueError as e:
        abort(400, description=str(e))