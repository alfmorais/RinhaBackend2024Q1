import sqlalchemy
from sqlalchemy import Column, Integer
from src.config.database import metadata

customers = sqlalchemy.Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("limit", Integer),
    Column("opening_balance", Integer),
)
