#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import os
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

TIME = '%Y-%m-%dT%H:%M:%S.%f'
Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(
            String(60),
            nullable=False,
            primary_key=True
        )
    created_at = Column(
            DateTime,
            default=datetime.utcnow(),
            nullable=False
        )
    updated_at = Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow()
        )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            print(kwargs)
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     TIME)
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     TIME)
            del kwargs['__class__']
            self.__dict__.update(kwargs)

        if not self.id:
            self.id = str(uuid.uuid4())
        d = datetime.now()
        if not self.created_at:
            self.created_at = self.updated_at = d
        if not self.updated_at:
            self.updated_at = d

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.strftime(TIME)
        dictionary['updated_at'] = self.updated_at.strftime(TIME)
        if dictionary.get("_sa_instance_state"):
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """
        to delete the current instance from the storage (models.storage)
        """
        models.storage.delete()
