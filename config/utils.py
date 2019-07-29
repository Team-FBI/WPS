from typing import Callable, List, Dict, Union
from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail, ValidationError


def response_error_handler(func: Callable) -> Callable:
    @wraps(func)
    def _wrapper(*args: List, **kwargs: Dict) -> Union[Callable, Response]:
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            e: BaseException
            err: BaseException
            res_code: int
            err = BaseException(
                "Unknow Interner server error",
                "We will log this and solve problem soon",
            )
            res_code = status.HTTP_423_LOCKED
            if isinstance(e, ConnectionRefusedError):
                err = e
                res_code = status.HTTP_405_METHOD_NOT_ALLOWED
            elif isinstance(e, PermissionError):
                err = e
                res_code = status.HTTP_401_UNAUTHORIZED
            elif isinstance(e, ValidationError):
                err = Exception(e.detail, "retype form data")
                res_code = status.HTTP_400_BAD_REQUEST
                return Response(data=err.args[0], status=res_code)
            elif isinstance(e, (AttributeError, ValueError)):
                err = e
                res_code = status.HTTP_400_BAD_REQUEST
            data = {"alert": err.args[0], "solution": err.args[-1]}
            return Response(data=data, status=res_code)

    return _wrapper

