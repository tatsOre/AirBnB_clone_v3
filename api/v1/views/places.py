#!/usr/bin/python3
"""
Module that creates a new view for 'Place' objects that handles all default
RestFul API actions: GET, DELETE, POST, PUT
"""
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def get_places(city_id=None, place_id=None):
    """Retrieves the list of all Place objects by city:
    GET /cities/<city_id>/places or by ID: GET /places/<place_id>"""
    city = storage.get(City, city_id)
    place = storage.get(Place, place_id)
    if city_id and city:
        return jsonify([place.to_dict() for place in city.places])
    elif place_id and place:
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a Place object: DELETE /api/v1/places/<place_id> by ID"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id=None):
    """Creates a Place: POST /api/v1/cities/<city_id>/places"""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in request_json:
        abort(400, {'Missing user_id'})
    elif 'name' not in request_json:
        abort(400, {'Missing name'})
    city = storage.get(City, city_id)
    user = storage.get(User, request_json['user_id'])
    if city_id and city and user:
        new_place = Place(**request_json)
        new_place.city_id = city_id
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """Updates a Place object: PUT /api/v1/places/<place_id> by ID"""
    place_attributes = request.get_json()
    if not place_attributes:
        abort(400, {'Not a JSON'})
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for attr, value in place_attributes.items():
        ignore = ['created_at', 'updated_at', 'id', 'user_id', 'city_id']
        if attr not in ignore:
            setattr(place, attr, value)
    storage.save()
    return jsonify(place.to_dict()), 200
