#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def retrieve_add_states():
    """Retrieves the list of all State objects and Creates a State"""
    if request.method == "GET":
        states = storage.all("State")
        states = [state.to_dict() for state in states.values()]
        return jsonify(states)

    if request.method == "POST":
        post_json = request.get_json()
        if not post_json:
            abort(404, "Not a JSON")
        if not post_json.get("name"):
            abort(400, "Missing name")
        state = State(**post_json)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def retrieve_delete_update(state_id=None):
    """
    Retrieves, deletes or updates a State object.
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if request.method == "GET":
        return jsonify(state.to_dict())

    if request.method == "DELETE":
        state.delete()
        return jsonify({})

    if request.method == "PUT":
        put_json = request.get_json()
        if not put_json:
            abort(404, "Not a JSON")
        for k, v in put_json.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(state, k, v)
        state.save()
    return jsonify(state.to_json()), 200
