from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
import sqlalchemy
from src.config.settings import DB_HOST, DB_NAME, DB_SECRET, DB_USERNAME
from src.models.customers import commands as customer_database_commands
from src.models.transactions import commands as transaction_database_commands
from starlette.applications import Starlette

metadata = sqlalchemy.MetaData()


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncGenerator:
    connection = await asyncpg.connect(
        user=DB_USERNAME,
        password=DB_SECRET,
        database=DB_NAME,
        host=DB_HOST,
    )

    for command in customer_database_commands:
        await connection.execute(command)

    for command in transaction_database_commands:
        await connection.execute(command)

    yield

    await connection.close()
