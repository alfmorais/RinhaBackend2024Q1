import datetime

import sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String
from src.config.database import metadata

transactions = sqlalchemy.Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("amount", Integer),
    Column("type", String(length=1)),
    Column("description", String(length=10)),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)
