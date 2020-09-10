#!/usr/bin/python3
"""
Module that creates a new view for 'City' objects that handles all default
RestFul API actions: GET, DELETE, POST, PUT
"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_cities(state_id=None, city_id=None):
    """Retrieves the list of all City objects: GET /states/<state_id>/cities
    or by ID: GET /cities/<city_id>"""
    city = storage.get(City, city_id)
    state = storage.get(State, state_id)
    if city_id and city:
        return city.to_dict()
    elif state_id and state:
        return jsonify([city.to_dict() for city in state.cities])
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id=None):
    """Deletes a City object: DELETE /api/v1/cities/<city_id> by ID"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id=None):
    """Creates a City: POST /api/v1/cities"""
    request_json = request.get_json()
    state = storage.get(State, state_id)
    if not request_json:
        abort(400, {'Not a JSON'})
    elif 'name' not in request_json:
        abort(400, {'Missing name'})
    elif state_id and state:
        request_json['state_id'] = state_id
        new_city = City(**request_json)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id=None):
    """Updates a City object: PUT /api/v1/cities/<city_id> by ID"""
    city_attributes = request.get_json()
    if not city_attributes:
        abort(400, {'Not a JSON'})
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for attr, value in city_attributes.items():
        if attr not in ['created_at', 'updated_at', 'id', 'state_id']:
            setattr(city, attr, value)
    storage.save()
    return jsonify(city.to_dict()), 200
