from backend import *

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table, MetaData, Float, DateTime
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

#setup db
engine = create_engine("sqlite:///budget.db", echo=True)
metadata = MetaData()


if not database_exists(engine.url):
    print("Creating db...")
    create_database(engine.url)


confirmations = Table(
    "confirmations", metadata,
    Column("id", Integer, primary_key=True),
    Column("token", String),
    Column("profile_id", Integer, ForeignKey("profiles.id")),
    sqlite_autoincrement=True
)


profiles = Table(
    "profiles", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("name", String),
    Column("gender", String),
    Column("dob", DateTime),
    Column("email", String),
    Column("password", String),
    Column("confirmed", Boolean),
    sqlite_autoincrement=True
)


transactions = Table(
    "transactions", metadata,
    Column("id", Integer, primary_key=True),
    Column("profile_id", Integer, ForeignKey("profiles.id")),
    Column("date_time", DateTime),
    Column("amount", Float),
    Column("comment", String),
    Column("inc_exp", String),
    Column("type", String),
    sqlite_autoincrement=True
)


recurring_transactions = Table(
    "recurring_transactions", metadata,
    Column("id", Integer, primary_key=True),
    Column("profile_id", Integer, ForeignKey("profiles.id")),
    Column("start_date_time", DateTime),
    Column("end_date_time", DateTime),
    Column("recurrence_value", Integer),
    Column("recurrence_type", String),
    Column("amount", Float),
    Column("comment", String),
    Column("inc_exp", String),
    Column("type", String),
    sqlite_autoincrement=True
)


limits = Table(
    "limits", metadata,
    Column("type", String, primary_key=True),
    Column("profile_id", Integer, ForeignKey("profiles.id"), primary_key=True),
    Column("amount", Float),
    Column("datetime", DateTime)
)


messages = Table(
    "messages", metadata,
    Column("id", Integer, primary_key=True),
    Column("profile_id", Integer, ForeignKey("profiles.id")),
    Column("recurring_transaction_id", Integer, ForeignKey("recurring_transactions.id")),
    Column("date_time", DateTime),
    sqlite_autoincrement=True
)


# during testing - drop all tables
try:
    confirmations.drop(engine)
    profiles.drop(engine)
    transactions.drop(engine)
    recurring_transactions.drop(engine)
    limits.drop(engine)
    messages.drop(engine)

except:
    pass


# add fresh tables
confirmations.create(engine)
profiles.create(engine)
transactions.create(engine)
recurring_transactions.create(engine)
limits.create(engine)
messages.create(engine)

