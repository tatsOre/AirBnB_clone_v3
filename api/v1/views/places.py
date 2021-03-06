#!/usr/bin/python3
"""
Module that creates a new view for 'Place' objects that handles all default
RestFul API actions: GET, DELETE, POST, PUT
"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
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


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places():
    """Search for a Place, rules:
    - If the HTTP request body is not valid JSON, will raise a 400 error.
    - If the JSON body is empty or each list of all keys are empty:
            will retrieve all hbnb 'Place' objects
    - If states list or cities list are not empty, will search for 'Place'
            objects inside each 'State' or 'City' ids listed. As states and
            cities are inclusive, the result will be all the places linked
            to each 'City' of a 'State' ID in the list.
    - If amenities list is not empty, will retrieve only the 'State' or 'City'
            places having all 'Amenity' ids listed. If states and cities list
            are empty, will search all hbnb 'Place' objects for a place
            having all 'Amenity' IDs listed"""
    search_parms = request.get_json()
    hbnb_places = storage.all(Place).values()  # All hbnb Place objects
    if search_parms is None:
        abort(400, {'Not a JSON'})
    if len(search_parms) == 0:
        return jsonify([place.to_dict() for place in hbnb_places])

    states = search_parms.get('states')
    cities = search_parms.get('cities')
    amenities = search_parms.get('amenities')
    if not states and not cities and not amenities:
        return jsonify([place.to_dict() for place in hbnb_places])

    state_cities = []  #  Stores cities for each state ID
    all_state_places = []  #  Stores all places in a state ID
    if states:
        for id in states:
            state = storage.get(State, id)
            if state:
                state_cities.extend([city for city in state.cities])
        for city in state_cities:
            for place in city.places:
                all_state_places.append(place)

    all_city_places = []  #  Stores all places in all cities
    if cities:
        for id in cities:
            city = storage.get(City, id)
            if city:
                all_city_places.extend([place for place in city.places])

    searched_places = []
    if amenities:
        if cities or states:
            places_to_search = all_state_places + all_city_places
        elif not cities and not states:
            places_to_search = hbnb_places
        for place in places_to_search:
            amen_list = [item.id for item in place.amenities]
            if all(i in amen_list for i in amenities):
                searched_places.append(place)
        return jsonify([place.to_dict() for place in searched_places])
    else:
        all_places = all_state_places + all_city_places
        return jsonify([place.to_dict() for place in all_places])


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
