import json
import urllib
import os
from dataclasses import dataclass
from bson import ObjectId

from flask import Flask, Response, jsonify

from pymongo import MongoClient
from pymodm.connection import connect
from dotenv import load_dotenv

from utils.models import Spot, Review

load_dotenv()
CONN_STR = f"mongodb+srv://illinoislabs:{urllib.parse.quote_plus(os.environ['MONGO_PASSWORD'])}@spotsdb.vayoj.mongodb.net/{urllib.parse.quote_plus(os.environ['MONGO_DB'])}?retryWrites=true&w=majority"
connect(CONN_STR)
conn = MongoClient(CONN_STR)
app = Flask(__name__)


@dataclass
class FlaskResponse:
    """
    Represents a Flask response.
    to_resp() a payload and a status code.
    """
    payload: Response
    code: int

    def to_resp(self):
        return self.payload, self.code


class JSONEncoder(json.JSONEncoder):
    """
    We create our own JSONEncoder to handle MongoDB IDs of type ObjectId
    when serializing objects.
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route("/")
def index():
    payload = {
        k: f"/{name.lower()}" for k, name in enumerate(conn["spots"].list_collection_names())
    }
    return FlaskResponse(jsonify({"documents": payload}), 200).to_resp()


@app.route("/spots")
def spots():
    # Get list of all spots in the database
    encoder = JSONEncoder()
    spots = [encoder.encode(x) for x in Spot.objects.all().values()]
    return FlaskResponse(
        jsonify(spots), 200
    ).to_resp()


if __name__ == "__main__":
    app.run('0.0.0.0', port=8000)
