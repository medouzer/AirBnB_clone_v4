#!/usr/bin/python3
"""states"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get all states"""
    dict_states = []
    states = storage.all(State).values()
    for state in states:
        dict_states.append(state.to_dict())
    return jsonify(dict_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_stateid(state_id):
    """get state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    dict_state = state.to_dict()
    return jsonify(dict_state)


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    """post method"""
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    if "name" not in req_data:
        abort(400, 'Missing name')
    state = State(**req_data)
    state.save()
    state_dict = state.to_dict()
    return jsonify(state_dict), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def put(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    for key, value in req_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    state_dict = state.to_dict()
    return jsonify(state_dict), 200
