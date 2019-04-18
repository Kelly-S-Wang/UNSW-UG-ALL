# This is python file for the profile/user class

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from .base import Base


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    gender = Column(String)
    dob = Column(DateTime)
    email = Column(String)
    password = Column(String)
    confirmed = Column(Boolean)


    def __init__(self, username, name, gender, dob, email, password, confirmed):
        self.username = username
        self.name = name
        self.gender = gender
        self.dob = dob
        self.email = email
        self.password = password
        self.confirmed = confirmed

    def set_id(self, value):
        self.id = value
        
    def set_username(self, value):
        self.username = value

    def set_name(self, value):
        self.name = value

    def set_gender(self, value):
        self.gender = value

    def set_dob(self, value):
        self.dob = value

    def set_email(self, value):
        self.email = value

    def set_password(self, value):
        self.password = value

    def set_confirmed(self, value):
        self.confirmed = value