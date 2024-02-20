from src.controllers.transactions import TransactionsController
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request


class CustomersTransactions(HTTPEndpoint):
    async def post(self, request: Request):
        customer_id = request.path_params["id"]
        payload = await request.json()

        controller = TransactionsController()
        response = controller.handle(payload, customer_id)
        return response
