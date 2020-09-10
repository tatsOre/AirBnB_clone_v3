#!/usr/bin/python3
"""
New view for Review objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/api/v1/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """ retrieve list of all Review objects """
    all_reviews = []
    if not storage.get('Place', place_id):
        abort(404)
    for review in storage.all('Review').values():
        if place_id == review.to_dict()['place_id']:
            all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/api/v1/reviews/<review_id>', strict_slashes=False)
def retrieve_review(review_id):
    """ retrieve a particular Review """
    review = storage.get('Review', review_id)
    if review:
        return review.to_dict()
    abort(404)


@app_views.route('/api/v1/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ delete a Review """
    review = storage.get('Review', review_id)
    if review:
        storage.delete(review)
        storage.save()
        return {}
    abort(404)


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create a Review """
    review_name = request.get_json()
    if not storage.get('Place', place_id):
        abort(404)
    if not review_name:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in review_name:
        abort(400, {'Missing user_id'})
    elif not storage.get('User', review_name['user_id']):
        abort(404)
    elif 'text' not in review_name:
        abort(400, {'Missing text'})
    review_name['place_id'] = place_id
    new_review = Review(**review_name)
    storage.new(new_review)
    storage.save()
    return new_review.to_dict(), 201
