#!/usr/bin/python3
"""amenities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """get all users"""
    users_list = []
    users = storage.all(User).values()
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """post new user"""
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    if "email" not in req_data:
        abort(400, 'Missing email')
    if "password" not in req_data:
        abort(400, 'Missing password')
    user = User(**req_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """update the user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    for key, value in req_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
