"""
Database Models

Schema: MongoDB
"""
from bson import SON
from pymodm import EmbeddedMongoModel, MongoModel, fields


class Review(EmbeddedMongoModel):
    """
    Review Model -- Represents a Review of a Study Spot
    """

    author = fields.CharField()
    rating = fields.FloatField()

    def __str__(self):
        return f"Review of {self.spot_id}: {self.rating} ({self.author})"


class Spot(MongoModel):
    """
    Spot Model -- Represents a Study Spot
    """

    name = fields.CharField()
    description = fields.CharField()
    reviews = fields.EmbeddedDocumentListField(Review, default=[])

    def __str__(self):
        return f"Spot {self.name}: {self.description}"
