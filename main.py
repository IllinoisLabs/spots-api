import json
import os
import urllib

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask
from pymodm.connection import connect

import config
from utils.models import Review, Spot

load_dotenv()


class JSONEncoder(json.JSONEncoder):
    """
    We create our own JSONEncoder to handle MongoDB IDs of type ObjectId
    when serializing objects.
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def create_app(config):
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(config)
        CONN_STR = f"mongodb+srv://illinoislabs:{urllib.parse.quote_plus(app.config['MONGO_PASSWORD'])}@spotsdb.vayoj.mongodb.net/{urllib.parse.quote_plus(app.config['MONGO_DB'])}?retryWrites=true&w=majority"
        connect(CONN_STR)

        from routes import route_blueprint

        app.register_blueprint(route_blueprint)
        app.json_encoder = JSONEncoder
    return app


if __name__ == "__main__":
    if os.environ["FLASK_ENV"] == "production":
        app = create_app(config.ProductionConfig)
    else:
        app = create_app(config.DevelopmentConfig)
    app.run("0.0.0.0", port=8000)
