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
    app.state.pool = await asyncpg.create_pool(
        user=DB_USERNAME,
        password=DB_SECRET,
        database=DB_NAME,
        host=DB_HOST,
        statement_cache_size=0,
        min_size=1,
        max_size=2,
        max_inactive_connection_lifetime=300,
        timeout=10,
    )
    """
    statement_cache_size: Evita problemas de statement caching
    min_size: Número mínimo de conexões no pool
    max_size: Número máximo de conexões no pool
    max_inactive_connection_lifetime: Tempo máximo em segundos para uma conexão ficar inativa
    timeout: Timeout em segundos para operações de banco de dados
    """

    async with app.state.pool.acquire() as conn, conn.transaction():
        for command in customer_database_commands:
            await conn.execute(command)

        for command in transaction_database_commands:
            await conn.execute(command)

    try:
        yield
    finally:
        await app.state.pool.close()
