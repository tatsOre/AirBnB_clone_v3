#!/usr/bin/python3
"""Module that set the routes and display request statuses"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status', strict_slashes=False)
def display_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=["GET"])
def count_hbnb_instances():
    """Retrieves the number of each objects by type"""
    hbnb_classes = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    response = {k: storage.count(v) for k, v in hbnb_classes.items()}
    return jsonify(response)
