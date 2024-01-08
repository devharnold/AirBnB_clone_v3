#!/usr/bin/python3

"""Start a Flask App"""
from flask import Flask, Blueprint, abort, jsonify, request, make_response
from models import User

app = Flask(__name__)
users_bp = Blueprint('users', __name__, url_prefix='/api/v1')

@users_bp.route('/users', methods=['GET'])
def get_users():
    """Retrieves the list of all user objects"""
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_userobj(user_id):
    """Retrieves a user object
    If user ID not linked to any object raise 404
    """
    user = User.query.get(user_id)
    if user_id is None:
        abort(404)
    return jsonify(user.to_dict())

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User Object
    If User ID not linked to any user object raise a 404 error
    Returns an empty dictionary with code 200
    """
    user = User.query.get(user_id)
    if user_id is None:
        abort(404)
    user.delete()
    return jsonify({}), 200

@users_bp.route('/users', methods=['POST'])
def create_user():
    """Creates a User
    Transform the HTTP body request to a dictionary
    If HTTP body request not a valid JSON raise a 400
    If no email in data -> raise 400, Missing Email
    """
    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()

    if 'email' not in data:
        abort(400, description='Missing email')
    if 'password' not in data:
        abort(400, description='Missing password')
    
    new_user = {
        'email': data['email'],
        'password': data['password']

    }
    return jsonify(new_user.to_dict), 201

@users_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User Object
    Transform the HTTP body request to a dictionary
    If the HTTP body request is not valid JSON, raise a 400
    Update the User object with all key-value pairs of the dictionary
    """
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        abort(400, description=str(e))