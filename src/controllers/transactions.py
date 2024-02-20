from typing import Dict

from pydantic_core import ValidationError
from src.schemas.transactions import Transactions
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED


class TransactionsController:
    def __init__(self, validate_class: Transactions = Transactions) -> None:
        self.validate_class = validate_class

    def validate_initial_payload(self, payload: Dict) -> Dict | Exception:
        try:
            schema = self.validate_class(**payload)
        except ValidationError as error:
            raise error.from_exception_data(
                title=error.args,
                line_errors=error.errors(),
            )

        return schema.json()

    def handle(self, payload: Dict, customer_id: str) -> Dict:
        validated_payload = self.validate_initial_payload(payload)
        response = {
            "validated_payload": validated_payload,
            "customer_id": customer_id,
        }
        """
        TODO: fazer a lógica de criar uma transação.
        """
        return JSONResponse(
            content=response,
            status_code=HTTP_201_CREATED,
        )
