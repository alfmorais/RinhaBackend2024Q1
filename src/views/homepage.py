from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse


class Homepage(HTTPEndpoint):
    async def get(self, request):
        return JSONResponse({"Hello": "World"})
