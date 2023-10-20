#!/usr/bin/python3
""" Place Module for HBNB project """
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from models.city import City
from models.user import User
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
    __reviews = relationship("Review", cascade="all, delete", backref="place")
    __amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        backref="place",
        viewonly=False
    )

    @property
    def reviews(self):
        """get all refiews with the current place id
        from filestorage
        """
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            return self.__reviews
        _list = [
            v for k, v in models.storage.all(models.Review).items()
            if v.place_id == self.id
        ]
        return (_list)

    @property
    def amenities(self):
        """get all amenities with the current place id
        """
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            return self.__amenities
        _list = [
            v for k, v in models.storage.all(models.Amenity).items()
            if v.id in self.amenity_ids
        ]
        return (_list)
