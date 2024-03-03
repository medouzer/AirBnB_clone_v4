#!/usr/bin/python3
"""places_reviews"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """get all reviews of places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """post a review to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    user_id = req_data.get("user_id")
    if user_id is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user not in None:
        abort(404)
    if "text" not in req_data:
        abort(400, 'Missing text')
    review = Review(place_id=place_id, **req_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """update review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    fix_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in fix_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
