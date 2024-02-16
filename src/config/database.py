from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
import sqlalchemy
from src.config.settings import DB_HOST, DB_NAME, DB_SECRET, DB_USERNAME
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
    yield
    await connection.close()
