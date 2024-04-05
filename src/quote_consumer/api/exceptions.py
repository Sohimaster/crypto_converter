from starlette import status


class BaseApiException(Exception):
    code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str = ""):
        self.message = message


class QuoteNotFound(BaseApiException):
    code: int = status.HTTP_404_NOT_FOUND


class RetryException(Exception):
    """Exception indicating the operation should retry."""
    pass


class StopException(Exception):
    """Exception indicating the operation should stop."""
    pass
