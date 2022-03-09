"""
Database Models

Schema: MongoDB
"""
from dataclasses import dataclass, asdict
from typing import Optional
import random


@dataclass
class Document:
    """
    Represents a valid MongoDB document.
    This is the parent class from which our other models
    will extend from.

    Default fields will be set here in the Document's __init__()
    method.
    """
    id: Optional[int]

    def __init__(self):
        self.id = random.randint(1000000, 9999999)  # TODO: Better ID selection

    def to_dict(self):
        return asdict(self)


@dataclass
class Spot(Document):
    """
    Spot Model -- Represents a Study Spot
    """
    name: str
    description: str

    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def __str__(self):
        return f"Spot {self.name}: {self.description}"

@dataclass
class Review(Document):
    """
    Review Model -- Represents a Review of a Study Spot
    """
    spot_id: int
    author: str
    rating: int

    def __init__(self, spot_id, author, rating):
        self.spot_id = spot_id
        self.author = author
        self.rating = rating

    def __str__(self):
        return f"Review of {self.spot_id}: {self.rating} ({self.author})"