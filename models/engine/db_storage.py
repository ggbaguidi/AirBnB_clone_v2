#!/usr/bin/python3
"""DBStorage"""
import os
from sqlalchemy import (
        create_engine,
        inspect)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from models.base_model import Base
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """database storage type"""
    __engine = None
    __session = None
    __classes = {
            "User": User,
            "State": State,
            "City":  City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
    __tables = ["State", "City", "User", "Place", "Review"]

    def __init__(self):
        """initialisation instance method"""
        dialect = "mysql"
        driver = "mysqldb"
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        database = os.getenv("HBNB_MYSQL_DB")
        mysql_db = {
                "drivername": dialect + "+" + driver,
                "username": user,
                "password": password,
                "host": host,
                "database": database,
                "port": 3306
            }
        self.__engine = create_engine(
                URL.create(**mysql_db),
                pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """get all records in database"""
        cls = cls if not isinstance(cls, str) else self.__classes.get(cls)
        records = {}
        cls_records = []
        if cls:
            cls_records = self.__session.query(cls).all()
            for row in cls_records:
                records[cls.__class__.__name__ + "." + row.id] = row

            return (records)
        for cls_, v in self.__classes.items():
            if cls_ in self.__tables:
                cls_records = self.__session.query(v).all()
            for row in cls_records:
                records[cls_ + "." + row.id] = row

        return records

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current  database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload storage"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
                sessionmaker(bind=self.__engine, expire_on_commit=False))()
