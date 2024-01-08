#!/usr/bin/python3

"""Start a Flask App"""
from flask import Blueprint, abort, jsonify, make_response, request
from models import City, State
from api.v1.views import app_views
states = [
    {'id': 1, 'name': 'State1'},
    {'id': 2, 'name': 'State2'},
]

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """Retrieves a list of all City objects"""
    state = City.query.get(state_id)
    if state is None:
        abort(404)

    cities = City.query.filter(state_id=state_id).all()
    cities_list = [city.to_dict() for city in cities]
    return jsonify(cities_list)

@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cityobj(city_id):
    """Retrieves a City Object
    If City ID not linked to any city object, raise 404"""
    city = City.query.get(city_id)
    if city_id is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object
    If City ID not linked to city object raise a 404
    Returns an empty dictionary with code 200
    """
    city = City.query.get(city_id)
    if city_id is None:
        abort(404)
    city.delete()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City object
    Transform HTTP requests to a dictionary
    If HTTP body request not a valid JSON, raise 400
    """
    state = next((s for s in states if s['id'] == state_id), None)
    if state is None:
        abort(404, description='State not found')

    if not request.is_json:
        abort(404, description='Not a JSON')

    data = request.get_json()

    if 'name' not in data:
        abort(400, description='Missing name')

    new_city = City(
        name = data['name'],
        state_id=state_id
    )
    new_city.save()
    return jsonify(new_city), 201

@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Updates a City object
    Transforms HTTP request to a dictionary
    If the HTTP request is not a valid JSON, raise 400
    If dictionary does not contain Key, raise 400 error
    """
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    
    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
