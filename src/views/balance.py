from src.controllers.balance import BalanceController
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse


class CustomersBalance(HTTPEndpoint):
    async def get(self, request: Request):
        customer_id = request.path_params["id"]

        controller = BalanceController()
        response = await controller.handle(customer_id)
        return response
