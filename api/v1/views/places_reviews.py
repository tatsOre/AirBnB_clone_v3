#!/usr/bin/python3
"""
New view for Review objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def get_reviews(place_id=None, review_id=None):
    """ retrieve list of all Review objects """
    place = storage.get(Place, place_id)
    review = storage.get(Review, review_id)
    if place_id and place:
        return jsonify([review.to_dict() for review in place.reviews])
    elif review_id and review:
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ delete a Review """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id=None):
    """ create a Review """
    request_json = request.get_json()
    if not request_json:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in request_json:
        abort(400, {'Missing user_id'})
    elif 'text' not in request_json:
        abort(400, {'Missing text'})
    place = storage.get(Place, place_id)
    user = storage.get(User, request_json['user_id'])
    if place_id and place and user:
        new_review = Review(**request_json)
        new_review.place_id = place_id
        new_review.save()
        return jsonify(new_review.to_dict()), 20
    else:
        abort(404)

@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id=None):
    """ update a Review """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    for key, value in update_attr.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
