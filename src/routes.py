from bson import ObjectId
from flask import Blueprint, jsonify, request
from pymodm.connection import _get_connection

from src.utils.models import Review, Spot

route_blueprint = Blueprint("route_blueprint", __name__)


@route_blueprint.route("/")
def index():
    conn = _get_connection()
    payload = {
        k: f"/{name.lower()}"
        for k, name in enumerate(conn.database.list_collection_names())
    }
    return jsonify({"documents": payload}), 200


@route_blueprint.route("/api/spots", methods=["GET", "POST"])
def spots():
    if request.method == "POST":
        # Post a spot to the database
        body = request.json
        if not ("name" in body) or not ("description" in body):
            return jsonify({"message": "Missing parameters"}), 400
        spot = Spot(name=body["name"], description=body["description"])
        spot.save()
        return jsonify(spot.to_son().to_dict()), 200
    else:
        # Get list of all spots in the database
        spots = [x for x in Spot.objects.all().values()]
        return jsonify(spots), 200


@route_blueprint.route("/api/spots/<id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def spot_by_id(id):
    if request.method == "PUT":
        body = request.json
        spot = Spot(_id=id)
        if "name" in body:
            spot.name = body["name"]
        if "description" in body:
            spot.description = body["description"]
        if "reviews" in body:
            for review in body["reviews"]:
                reviewModel = Review(author=review["author"], rating=review["rating"])
                spot.reviews.append(reviewModel)
        spot.save()
        return jsonify(spot.to_son().to_dict()), 200

    elif request.method == "PATCH":
        body = request.json
        try:
            spot = Spot.objects.get({"_id": ObjectId(id)})
        except Spot.DoesNotExist:
            return jsonify({"message": "Spot not found"}), 404
        if "name" in body:
            spot.name = body["name"]
        if "description" in body:
            spot.description = body["description"]
        if "reviews" in body:
            spot.reviews = []
            for review in body["reviews"]:
                reviewModel = Review(author=review["author"], rating=review["rating"])
                spot.reviews.append(reviewModel)
        spot.save()
        return jsonify(spot.to_son().to_dict()), 200

    elif request.method == "DELETE":
        spot = Spot.objects.raw({"_id": ObjectId(id)})
        spot.delete()
        return jsonify({"message": "Spot deleted"}), 204

    else:
        try:
            spot = Spot.objects.get({"_id": ObjectId(id)})
            return jsonify(spot.to_son().to_dict()), 200

        except Spot.DoesNotExist:
            return jsonify({"message": "Spot not found"}), 404
