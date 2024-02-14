from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse


class CustomersTransactions(HTTPEndpoint):
    async def post(self, request):
        customer_id = request.path_params["id"]
        return JSONResponse({"customer_id": customer_id})
