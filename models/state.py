#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    if not os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            all_cities = list(models.storage.all(City).values())
            return list(filter((lambda c: c.state_id == self.id), all_cities))
