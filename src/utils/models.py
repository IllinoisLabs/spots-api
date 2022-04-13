"""
Database Models

Schema: MongoDB
"""
from pymodm import MongoModel, fields


class Spot(MongoModel):
    """
    Spot Model -- Represents a Study Spot
    """

    name = fields.CharField()
    description = fields.CharField()

    def __str__(self):
        return f"Spot {self.name}: {self.description}"


class Review(MongoModel):
    """
    Review Model -- Represents a Review of a Study Spot
    """

    spot_id = fields.ReferenceField(Spot)
    author = fields.CharField()
    rating = fields.FloatField()

    def __str__(self):
        return f"Review of {self.spot_id}: {self.rating} ({self.author})"
