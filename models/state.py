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
        def create(self):
            """getter attribute cities"""
            s = []
            for _, val in models.storagege.all(City).items():
                if val.state_id == State.id:
                    s.append(val)
            return s
