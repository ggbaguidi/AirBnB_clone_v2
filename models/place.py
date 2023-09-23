#!/usr/bin/python3
""" Place Module for HBNB project """
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from models.city import City
from models.user import User
from models.amenity import Amenity
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey(City.id), nullable=False)
    user_id = Column(String(60), ForeignKey(User.id), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    reviews = relationship("Review", cascade="all, delete", backref="place")
    amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False)

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """Returns respective list of reviews"""
            all_reviews = models.storage.all(models.review.Review)
            return list(filter((lambda c: c.place_id == self.id), all_reviews))

        @property
        def amenities(self):
            """Returns respective list of reviews"""
            amenities = models.storage.all(models.amenity.Amenity)
            return list(filter((lambda c: c.place_id == self.id), amenities))
