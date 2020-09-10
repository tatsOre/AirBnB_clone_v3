#!/usr/bin/python3
"""
New view for User objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=["GET"])
def all_users():
    """ Retrieves list of all User objects """
    all_users = []
    for user in storage.all(User).values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=["GET"])
def retrieve_user(user_id):
    """ Retrieves a particular User """
    try:
        user = jsonify(storage.get(User, user_id).to_dict())
        return user
    except:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User """
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Creates a User """
    user_name = request.get_json()
    if not user_name:
        abort(400, {'Not a JSON'})
    elif 'email' not in user_name:
        abort(400, {'Missing email'})
    elif 'password' not in user_name:
        abort(400, {'Missing password'})
    new_user = User(**user_name)
    storage.new(new_user)
    storage.save()
    return new_user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates a User """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_user = storage.get(User, user_id)
    if not my_user:
        abort(404)
    for key, value in update_attr.items():
        if key not in ['created_at', 'updated_at', 'id', 'email']:
            setattr(my_user, key, value)
    storage.save()
    return my_user.to_dict(), 200
