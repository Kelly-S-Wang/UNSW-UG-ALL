# This is a python file for transaction class

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from .base import Base

class Limit(Base):
    __tablename__ = "limits"
    type = Column(String, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), primary_key=True)
    amount = Column(Float)
    datetime = Column(DateTime)

    def __init__(self, type, profile_id, amount, datetime):
        self.type = type
        self.profile_id = profile_id
        self.amount = amount
        self.datetime = datetime

    def set_type(self, value):
        self.type = value

    def set_profile_id(self, value):
        self.profile_id = value

    def set_amount(self, value):
        self.amount = value

    def set_datetime(self, value):
        self.datetime = value