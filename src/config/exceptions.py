from pydantic_core import ValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST


async def json_exception(request: Request, exc: HTTPException):
    return JSONResponse(content=exc.detail, status_code=HTTP_400_BAD_REQUEST)


async def validation_error(request: Request, exc: ValidationError):
    return JSONResponse(content=exc.errors(), status_code=HTTP_400_BAD_REQUEST)


exception_handlers = {
    HTTPException: json_exception,
    ValidationError: validation_error,
}
