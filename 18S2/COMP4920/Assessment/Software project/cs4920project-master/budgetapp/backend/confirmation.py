# This is python file for the confirmation class

from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Confirmation(Base):
    __tablename__ = "confirmations"
    id = Column(Integer, primary_key=True)
    token = Column(String)
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    def __init__(self, token, profile_id):
        self.token = token
        self.profile_id = profile_id

    def set_id(self, value):
        self.id = value

    def set_token(self, value):
        self.token = value

    def set_profile_id(self, value):
        self.profile_id = value