#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def retrieve_add_amenities():
    """Retrieves the list of all Amenity objects and Creates a Amenity"""
    if request.method == "GET":
        amenities = storage.all("Amenity")
        amenities = [amenity.to_dict() for amenity in amenities.values()]
        return jsonify(amenities)

    if request.method == "POST":
        post_json = request.get_json()
        if not post_json:
            abort(404, "Not a JSON")
        if not post_json.get("name"):
            abort(400, "Missing name")
        amenity = Amenity(**post_json)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def retrieve_delete_update(amenity_id=None):
    """
    Retrieves, deletes or updates a Amenity object.
    """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if request.method == "GET":
        return jsonify(amenity.to_dict())

    if request.method == "DELETE":
        amenity.delete()
        return jsonify({})

    if request.method == "PUT":
        put_json = request.get_json()
        if not put_json:
            abort(404, "Not a JSON")
        for k, v in put_json.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(amenity, k, v)
        amenity.save()
    return jsonify(amenity.to_json()), 200
