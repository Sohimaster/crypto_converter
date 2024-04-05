from fastapi import responses
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request

from quote_consumer.api.exceptions import BaseApiException


def base_api_exception_handler(_: Request, error: BaseApiException) -> responses.JSONResponse:
    return responses.JSONResponse(
        content={"message": error.message},
        status_code=error.code,
    )


def validation_exception_handler(_: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": error["loc"][-1],
            "error": error["msg"]
        })

    return responses.JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors},
    )
