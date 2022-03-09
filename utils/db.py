"""
Database Functions

Schema: MongoDB
"""
from pydoc import Doc
import urllib
import os
from dataclasses import dataclass

from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv

from .models import Document, Spot

load_dotenv()


@dataclass
class Connection:
    client: MongoClient
    db: Database
    CONN_STR = f"mongodb+srv://illinoislabs:{urllib.parse.quote_plus(os.environ['MONGO_PASSWORD'])}@spotsdb.vayoj.mongodb.net/{urllib.parse.quote_plus(os.environ['MONGO_DB'])}?retryWrites=true&w=majority"

    def __init__(self):
        # Sets member variables to client and database connection
        self.client = MongoClient(self.CONN_STR)
        self.db = self.client["spots"]


def insert_one(conn: Connection, collection: str, document: Document):
    if not collection in conn.db.list_collection_names():
        # Invalid collection name
        print(f"[ ERROR ]: Collection {collection} does not exist.")
        return
    col = conn.db[collection]
    doc = document.to_dict()
    col.insert_one(doc)
    # Return inserted document
    return doc


if __name__ == "__main__":
    from models import Document, Spot
    conn = Connection()  # Establish new database connection
    brewlab = Spot(name="Legends", description="Legends: Bar and Grill is a bar.")
    insert_one(conn, "Spot", brewlab)
