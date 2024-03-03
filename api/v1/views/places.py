#!/usr/bin/python3
"""amenities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """get all places of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """post a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    if "user_id" not in req_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, req_data["user_id"])
    if user is None:
        abort(404)
    if "name" not in req_data:
        abort(400, 'Missing name')
    place = Place(city_id=city_id, **req_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """update place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    for key, value in req_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
