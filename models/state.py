#!/usr/bin/python3
# KASPER edited @ 10/31 12:03
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
)


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan",
                          primaryjoin='State.id == City.state_id')

    @property
    def cities(self):
        new_dict = {}
        a = storage.all()
        for key in a:
            b = a[key].to_dict()
            if b['__class__'] == 'City' and b['state_id'] == self.id:
                new_dict.update({key: a[key]})
        return new_dict
