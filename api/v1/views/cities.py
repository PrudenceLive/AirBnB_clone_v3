#!/usr/bin/python3
"""View for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def retrieve_add_state_cities():
    """Retrieves the list of all City objects of a state
    and Creates a City"""
    city_state = storage.get("State", state_id)

    if not city_state:
        abort(404)

    if request.method == "GET":
        cities = storage.all("City")
        state_cities = [city.to_dict() for city in cities.values()
                        if city.state_id == state_id]
        return jsonify(state_cities)

    if request.method == "POST":
        post_json = request.get_json()
        if not post_json:
            abort(404, "Not a JSON")
        if not post_json.get("name"):
            abort(400, "Missing name")
        post_json["state_id"] = state_id
        city = City(**post_json)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def retrieve_delete_update(city_id=None):
    """
    Retrieves, deletes or updates a City object.
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    if request.method == "DELETE":
        city.delete()
        return jsonify({})

    if request.method == "PUT":
        put_json = request.get_json()
        if not put_json:
            abort(404, "Not a JSON")
        for k, v in put_json.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, k, v)
        city.save()
    return jsonify(city.to_json()), 200
