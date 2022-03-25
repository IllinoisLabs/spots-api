import json
import os
import urllib

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, Response, g, jsonify, request
from pymodm.connection import _get_connection, connect

from utils.models import Review, Spot

load_dotenv()
CONN_STR = f"mongodb+srv://illinoislabs:{urllib.parse.quote_plus(os.environ['MONGO_PASSWORD'])}@spotsdb.vayoj.mongodb.net/{urllib.parse.quote_plus(os.environ['MONGO_DB'])}?retryWrites=true&w=majority"
connect(CONN_STR)
app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    """
    We create our own JSONEncoder to handle MongoDB IDs of type ObjectId
    when serializing objects.
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app.json_encoder = JSONEncoder


@app.route("/")
def index():
    conn = _get_connection()
    payload = {
        k: f"/{name.lower()}"
        for k, name in enumerate(conn.database.list_collection_names())
    }
    return jsonify({"documents": payload}), 200


@app.route("/api/spots", methods=["GET", "POST"])
def spots():
    if request.method == "POST":
        # Post a spot to the database
        body = request.json
        if not "name" in body or not "description" in body:
            return jsonify({"message": "Missing parameters"}, 400)
        spot = Spot(name=body["name"], description=body["description"])
        spot.save()
        return jsonify(spot.to_son().to_dict()), 200
    else:
        # Get list of all spots in the database
        spots = [x for x in Spot.objects.all().values()]
        return jsonify(spots), 200


@app.route("/api/spots/<id>", methods=["GET", "PUT", "DELETE"])
def spot_by_id(id):
    if request.method == "PUT":
        body = request.json
        try:
            spot = Spot.objects.get({"_id": ObjectId(id)})
        except Spot.DoesNotExist:
            return jsonify({"message": "Spot not found"}), 404
        if "name" in body:
            spot.name = body["name"]
        if "description" in body:
            spot.description = body["description"]
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


if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)
