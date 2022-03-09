import json
from dataclasses import dataclass
from bson import ObjectId

from flask import Flask, Response, jsonify

from utils.db import Connection

app = Flask(__name__)

# Establish database connection
conn = Connection()


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
        k: f"/{name.lower()}" for k, name in enumerate(conn.db.list_collection_names())
    }
    return FlaskResponse(jsonify({"documents": payload}), 200).to_resp()


@app.route("/spot")
def spots():
    # Get list of all spots in the database
    spots = conn.db["Spot"]
    encoder = JSONEncoder()
    return FlaskResponse(
        jsonify([encoder.encode(x) for x in spots.find()]), 200
    ).to_resp()


if __name__ == "__main__":
    app.run('0.0.0.0', port=8000)
