#!/usr/bin/python3
from flask import Flask, Blueprint, abort, jsonify, request, make_response
from models import State

app = Flask(__name__)
states_bp = Blueprint('states', __name__, url_prefix='/api/v1')

@states_bp.route('/states', methods=['GET'])
def get_states():
    """Retrieves a list of all states
    """
    states = State.query.all()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)

@states_bp.route('/states/<state_id>', methods=['GET'])
def get_stateobj(state_id):
    """Retrieves a State Object
    If State ID not linked to any state object raise 404
    """
    state = State.query.get(state_id)
    if state_id is None:
        abort(404)
    return jsonify(state.to_dict())

@states_bp.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a state object
    If State ID not linked to any state object, raise a 404
    """
    state = State.query.get(state_id)
    if state_id is None:
        abort(404)
    state.delete()
    return jsonify({})

@states_bp.route('/states', methods=['POST'])
def create_state():
    """Creates a State
    Transform HTTP body request to a dictionary
    If the HTTP body request not a valid JSON, raise 400
    """
    if not request.json or not 'title' in request.json:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Not a JSON")
        return jsonify({"message": "New State Created!"}), 201
    
    except ValueError as e:
        abort(400, description=str(e))
    return jsonify({"message": "Missing name"}), 400

@states_bp.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    """Updates a State Object
    Transform HTTP request to a dictionary
    If the HTTP body request not a valid JSON raise 400
    """
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    except ValueError as e:
        abort(400, description=str(e))
