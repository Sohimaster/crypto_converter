from fastapi import responses
from starlette.requests import Request

from quote_consumer.api.exceptions import BaseApiException


def base_api_exception_handler(_: Request, error: BaseApiException) -> responses.JSONResponse:
    return responses.JSONResponse(
        content={"message": error.message},
        status_code=error.code,
    )
