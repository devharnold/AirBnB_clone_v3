#!/usr/bin/python3

"""Start a Flask App"""
from flask import Flask, Blueprint, abort, jsonify, request, make_response
from models import Amenity

app = Flask(__name__)
amenity_bp = Blueprint('amenities', __name__, url_prefix='/api/v1')

@amenity_bp.route('/amenities', methods=['GET'])
def get_amenities():
    """Retrieves a list of amenity objects"""
    amenities = Amenity.query.all()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)

@amenity_bp.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenityobj(amenity_id):
    """Retrieves a Amenity object
    If Amenity ID is not linked to any Amenity object, raise a 404
    """
    amenity = Amenity.query.get(amenity_id)
    if amenity_id is None:
        abort(404)
    return jsonify(amenity.to_dict())

@amenity_bp.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object
    Transforms HTTP request to a dictionary
    If the HTTP request is not a valid JSON, raise 400
    """
    amenity = Amenity.query.get(amenity_id)
    if amenity_id is None:
        abort(404)
    amenity.delete()
    return jsonify({}), 200

@amenity_bp.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a Amenity
    Transforms HTTP request to a dictionary
    If HTTP request not a valid JSON, raise 400
    If dictionary does not contain name, raise 400
    """
    if not request.is_json:
        abort(404, description='Not a JSON')

    data = request.get_json()

    if 'name' not in data:
        abort(400, description='Missing name')

    new_amenity = {
        'name': data['name']
    }
    return jsonify(new_amenity.to_dict()), 201
    
@amenity_bp.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity
    Transform HTTP request to a dictionary
    Update the Amenity object with all the key-value pairs of the dictionary
    """
    amenity = Amenity.query.get(amenity_id)
    if amenity is None:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    
    except ValueError as e:
        abort(400, description=str(e))