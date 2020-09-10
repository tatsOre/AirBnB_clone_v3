#!/usr/bin/python3
"""
Module that creates a new view for 'State' objects that handles all default
RestFul API actions: GET, DELETE, POST, PUT
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["GET"])
@app_views.route('/states', strict_slashes=False, methods=["GET"])
def get_states(state_id=None):
    """Retrieves the list of all State objects: GET /api/v1/states or by ID"""
    if state_id:
        state = storage.get(State, state_id)
        if state:
            return state.to_dict()
        else:
            abort(404)
    else:
        all_states = storage.all(State).values()
        return jsonify([state.to_dict() for state in all_states])


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object: DELETE /api/v1/states/<state_id> by ID"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=["POST"])
def create_state():
    """Creates a State: POST /api/v1/states"""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'Not a JSON'})
    elif 'name' not in request_json:
        abort(400, {'Missing name'})
    new_state = State(**request_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["PUT"])
def update_state(state_id=None):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    state_attributes = request.get_json()
    if not state_attributes:
        abort(400, {'Not a JSON'})
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for attr, value in state_attributes.items():
        if attr not in ['created_at', 'updated_at', 'id']:
            setattr(state, attr, value)
    storage.save()
    return jsonify(state.to_dict()), 200
