# this is a python file for message class, used for recurring transaction reminder

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from .base import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    recurring_transaction_id = Column(Integer, ForeignKey("recurring_transactions.id"))
    date_time = Column(DateTime)

    def __init__(self, profile_id, recurring_transaction_id, date_time):
        self.profile_id = profile_id
        self.recurring_transaction_id = recurring_transaction_id
        self.date_time = date_time

    def set_profile_id(self, value):
        self.profile_id = value

    def set_recurring_transaction_id(self, value):
        self.recurring_transaction_id = value