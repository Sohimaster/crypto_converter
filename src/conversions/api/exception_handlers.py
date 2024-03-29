from fastapi import responses
from starlette import status
from starlette.requests import Request

from conversions.api.exceptions import BaseApiException


def base_api_exception_handler(_: Request, error: BaseApiException) -> responses.JSONResponse:
    return responses.JSONResponse(
        content={"message": error.message},
        status_code=status.HTTP_400_BAD_REQUEST,
    )
