from pydantic_core import ValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


class NotFoundCustomerException(Exception):
    message = {"error": "Customer not found"}


class TransactionCreateExecption(Exception):
    message = {"error": "Amount requested exceed account limit"}


async def json_exception(
    request: Request,
    exc: HTTPException,
):
    return JSONResponse(
        content=exc.detail,
        status_code=HTTP_400_BAD_REQUEST,
    )


async def validation_error(
    request: Request,
    exc: ValidationError,
):
    return JSONResponse(
        content=exc.errors(),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def not_found_customer_exception(
    request: Request,
    exc: NotFoundCustomerException,
):
    return JSONResponse(
        content=exc.message,
        status_code=HTTP_404_NOT_FOUND,
    )


async def transaction_create_exception(
    request: Request,
    exc: TransactionCreateExecption,
):
    return JSONResponse(
        content=exc.message,
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


exception_handlers = {
    # HTTPException: json_exception,
    ValidationError: validation_error,
    NotFoundCustomerException: not_found_customer_exception,
    TransactionCreateExecption: transaction_create_exception,
}
