# This is a python file for transaction class

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from .base import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    date_time = Column(DateTime)
    amount = Column(Float)
    comment = Column(String)
    inc_exp = Column(String)
    type = Column(String)

    def __init__(self, profile_id, date_time, amount, comment, inc_exp, type):
        self.profile_id = profile_id
        self.date_time = date_time
        self.amount = amount
        self.comment = comment
        self.inc_exp = inc_exp
        self.type = type

    # id, profile_id should be immutable
    #
    # def set_id(self, value):
    #     self.id = value
    #
    # def set_profile_id(self, value):
    #     self.profile_id = value

    def set_date_time(self, value):
        self.date_time = value

    def set_amount(self, value):
        self.amount = value

    def set_comment(self, value):
        self.comment = value

    def set_inc_exp(self, value):
        self.inc_exp = value

    def set_type(self, value):
        self.type = value

