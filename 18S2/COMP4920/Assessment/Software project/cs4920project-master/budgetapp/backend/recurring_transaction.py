# this is a python file for recurring transaction class

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from .base import Base

class Recurring_transaction(Base):
    __tablename__ = "recurring_transactions"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    start_date_time = Column(DateTime)
    end_date_time = Column(DateTime)
    recurrence_value = Column(Integer)
    recurrence_type = Column(String)
    amount = Column(Float)
    comment = Column(String)
    inc_exp = Column(String)
    type = Column(String)

    def __init__(self, profile_id, start_date_time, end_date_time, recurrence_value, recurrence_type, amount, comment, inc_exp, type):
        self.profile_id = profile_id
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.recurrence_value = recurrence_value
        self.recurrence_type = recurrence_type
        self.amount = amount
        self.comment = comment
        self.inc_exp = inc_exp
        self.type = type

    # immutable
    # def set_profile_id(self, value):
    #     self.profile_id = value

    def set_start_date_time(self, value):
        self.start_date_time = value

    def set_end_date_time(self, value):
        self.end_date_time = value

    def set_recurrence_value(self, value):
        self.recurrence_value = value

    def set_recurrence_type(self, value):
        self.recurrence_type = value

    def set_amount(self, value):
        self.amount = value

    def set_comment(self, value):
        self.comment = value

    def set_inc_exp(self, value):
        self.inc_exp = value

    def set_type(self, value):
        self.type = value

