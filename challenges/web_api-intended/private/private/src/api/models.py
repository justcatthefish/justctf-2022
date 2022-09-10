#! /usr/bin/env python3

# DB helpers for creating and operating on database

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class User(Model):
    """
    Class implementing user object in DB
    """
    __tablename__ = "users"

    idx = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)


class Inventory(Model):
    """
    Class implementing inventory items in DB
    """
    __tablename__ = 'items'
    idx = Column(Integer, index=True, primary_key=True)
    name = Column(String, unique=True, index=True)
    quantity = Column(Integer)
    user_manual_ref = Column(String)

    def as_dict(self):
        return {'id': self.idx, 'name': self.name, 'quantity': self.quantity, 'user_manual_ref': self.user_manual_ref}