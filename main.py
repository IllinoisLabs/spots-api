import json
import urllib
import os
from bson import json_util

from flask import Flask, Response, jsonify

from pymodm.connection import connect, _get_connection
from dotenv import load_dotenv

from utils.models import Spot, Review

load_dotenv()
CONN_STR = f"mongodb+srv://illinoislabs:{urllib.parse.quote_plus(os.environ['MONGO_PASSWORD'])}@spotsdb.vayoj.mongodb.net/{urllib.parse.quote_plus(os.environ['MONGO_DB'])}?retryWrites=true&w=majority"
connect(CONN_STR)
app = Flask(__name__)

@app.route("/")
def index():
    conn = _get_connection()
    payload = {
        k: f"/{name.lower()}" for k, name in enumerate(conn.database.list_collection_names())
    }
    return jsonify({"documents": payload}), 200


@app.route("/spots")
def spots():
    # Get list of all spots in the database
    spots = [x for x in Spot.objects.all().values()]
    return Response(
        response=json_util.dumps(spots),
        status=200,
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run('0.0.0.0', port=8000)
