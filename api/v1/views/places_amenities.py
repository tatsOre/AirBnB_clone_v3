#!/usr/bin/python3
"""
Module that creates a new view for 'Place/Amenity' relationship objects
that handles all default RestFul API actions: GET, DELETE, POST, PUT
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_place(place_id=None):
    """Retrieves the list of all Amenity objects by Place ID:
    GET /places/<place_id>/amenities"""
    place = storage.get(Place, place_id)
    if place and place_id:
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_in_place(place_id=None, amenity_id=None):
    """Deletes an Amenity object to a Place:
    DELETE /api/v1/places/<place_id>/amenities/<amenity_id>"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity and amenity in place.amenities:
        place.amenities.remove(amenity)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity_in_place(place_id=None, amenity_id=None):
    """Creates an Amenity object to a Place:
    POST /places/<place_id>/amenities/<amenity_id>"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    else:
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
