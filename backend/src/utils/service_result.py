import logging
import inspect
from fastapi import Response

from .app_exceptions import AppExceptionCase


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


class ServiceResult(object):
    def __init__(self, arg, headers=None):
        if isinstance(arg, AppExceptionCase):
            self.success = False
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
        self.headers = headers or {}
        self.value = arg

    def __str__(self):
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_case}>"

    def handle(self, response: Response | None = None):
        logger = logging.getLogger("service")
        if response is not None:
            response.headers.update(self.headers)
        if not self.success:
            logger.error(f"{self.value} | caller={caller_info()}")
            raise self.value
        return self.value
