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
    place_id = fields.CharField()

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

class GoogleBusinessModel(MongoModel):
    """
        Places Model -- Represents the Google Business Signature of a Spot
    """
    spot_id = fields.ReferenceField(Spot)
    name = fields.CharField()
    formatted_address = fields.CharField()
    geometry = fields.PointField() #[lat,long]
    types = fields.ListField() #[bar, restaurant, etc]

    def __str__(self):
        return f"Business: {self.name}\nAddress: {self.formatted_address}\n"
    