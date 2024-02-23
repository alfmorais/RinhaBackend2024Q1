from datetime import datetime
from typing import Awaitable, Dict

import asyncpg
from src.config.exceptions import NotFoundCustomerException
from src.config.settings import DB_HOST, DB_NAME, DB_SECRET, DB_USERNAME
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK


class BalanceController:
    async def retrieve_customer_from_database(
        self,
        connection: Awaitable,
        customer_id: str,
    ) -> Dict | NotFoundCustomerException:
        query = "SELECT * FROM clientes WHERE id = {};".format(customer_id)
        customer = await connection.fetchrow(query)

        if customer is None:
            raise NotFoundCustomerException

        return dict(customer)

    async def retrive_transactions_from_database(
        self,
        connection: Awaitable,
        customer_id: str,
    ) -> Dict:
        query = """
            SELECT * FROM Transacoes
            WHERE cliente_id = {}
            ORDER BY realizada_em DESC LIMIT 10;
        """.format(
            customer_id
        )
        transactions = await connection.fetch(query)

        if transactions is None:
            return []

        response = [
            {
                "valor": transaction["valor"],
                "tipo": transaction["tipo"],
                "descricao": transaction["descricao"],
                "realizada_em": transaction["realizada_em"].isoformat(),
            }
            for transaction in transactions
        ]
        return response

    async def response(self, customer, transactions):
        response = {
            "saldo": {
                "total": customer["saldo"],
                "data_extrato": datetime.now().isoformat(),
                "limite": customer["limite"],
            },
            "ultimas_transacoes": transactions,
        }
        return response

    async def handle(self, customer_id):
        connection = await asyncpg.connect(
            user=DB_USERNAME,
            password=DB_SECRET,
            database=DB_NAME,
            host=DB_HOST,
        )
        customer = await self.retrieve_customer_from_database(
            connection,
            customer_id,
        )
        transactions = await self.retrive_transactions_from_database(
            connection,
            customer_id,
        )

        response = await self.response(customer, transactions)

        return JSONResponse(
            content=response,
            status_code=HTTP_200_OK,
        )
