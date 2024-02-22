import json
from typing import Awaitable, Dict

import asyncpg
from pydantic_core import ValidationError
from src.config.exceptions import (
    NotFoundCustomerException,
    TransactionCreateExecption,
)
from src.config.settings import DB_HOST, DB_NAME, DB_SECRET, DB_USERNAME
from src.schemas.transactions import Transactions
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK


class TransactionsController:
    def __init__(self, validate_class: Transactions = Transactions) -> None:
        self.validate_class = validate_class

    async def validate_payload(self, payload: Dict) -> Dict | ValidationError:
        try:
            schema = self.validate_class(**payload)
        except ValidationError as error:
            raise error.from_exception_data(
                title=error.args,
                line_errors=error.errors(),
            )

        response = json.loads(schema.json())
        return response

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

    async def condition_to_not_create_transaction(
        self,
        new_customer_balance: int,
        customer_limit: int,
    ) -> bool:
        if new_customer_balance < 0:
            balance = new_customer_balance * (-1)
            return balance > customer_limit

        return False

    async def query_create_transaction(
        self,
        transaction_amount: int,
        transaction_type: str,
        transaction_description: str,
        customer_id: int,
    ) -> str:
        query = """
            INSERT INTO Transacoes (valor, tipo, descricao, cliente_id)
            VALUES ({}, '{}', '{}', {})
            RETURNING id;
        """.format(
            transaction_amount,
            transaction_type,
            transaction_description,
            customer_id,
        )
        return query

    async def query_update_customer(
        self,
        new_customer_balance: int,
        customer_id: int,
    ) -> str:
        query = """
            UPDATE Clientes
            SET saldo_inicial = {}
            WHERE id = {};
        """.format(
            new_customer_balance,
            customer_id,
        )
        return query

    async def response(
        self,
        customer_limit: int,
        new_customer_balance: int,
    ) -> Dict:
        response = {
            "limite": customer_limit,
            "saldo": new_customer_balance,
        }
        return response

    async def credit_operation(
        self,
        connection: Awaitable,
        validated_payload: Dict,
        customer: Dict,
    ) -> Dict | TransactionCreateExecption:
        """
        Um crédito (C) faz o oposto: diminui o saldo destas contas.
        """
        transaction_amount = validated_payload["amount"]
        customer_limit = customer["limite"]
        customer_balance = customer["saldo_inicial"]
        new_customer_balance = customer_balance - transaction_amount

        condition = await self.condition_to_not_create_transaction(
            new_customer_balance,
            customer_limit,
        )

        if condition:
            raise TransactionCreateExecption

        transaction_type = validated_payload["type"]
        transaction_description = validated_payload["description"]
        customer_id = customer["id"]

        query_transaction_create = await self.query_create_transaction(
            transaction_amount,
            transaction_type,
            transaction_description,
            customer_id,
        )
        await connection.execute(query_transaction_create)

        query_update_customer = await self.query_update_customer(
            new_customer_balance,
            customer_id,
        )
        await connection.execute(query_update_customer)

        response = await self.response(
            customer_limit,
            new_customer_balance,
        )
        return response

    async def debit_operation(
        self,
        connection: Awaitable,
        validated_payload: Dict,
        customer: Dict,
    ) -> Dict | Exception:
        """
        Um débito (D) aumenta o saldo de um ativo e de uma conta de despesas.
        """
        transaction_amount = validated_payload["amount"]
        customer_balance = customer["saldo_inicial"]
        customer_limit = customer["limite"]
        new_customer_balance = customer_balance + transaction_amount

        transaction_type = validated_payload["type"]
        transaction_description = validated_payload["description"]
        customer_id = customer["id"]

        query_transaction_create = await self.query_create_transaction(
            transaction_amount,
            transaction_type,
            transaction_description,
            customer_id,
        )
        await connection.execute(query_transaction_create)

        query_update_customer = await self.query_update_customer(
            new_customer_balance,
            customer_id,
        )
        await connection.execute(query_update_customer)

        response = await self.response(
            customer_limit,
            new_customer_balance,
        )
        return response

    async def handle(self, payload: Dict, customer_id: str) -> Dict:
        validated_payload = await self.validate_payload(payload)

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

        type_operation = validated_payload["type"]
        operation = {
            "c": self.credit_operation,
            "d": self.debit_operation,
        }

        response = await operation[type_operation](
            connection,
            validated_payload,
            customer,
        )

        return JSONResponse(
            content=response,
            status_code=HTTP_200_OK,
        )
