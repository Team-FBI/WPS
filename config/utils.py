from typing import Callable, List, Dict
from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail, ValidationError


def response_error_handler(func: Callable) -> Callable:
    @wraps(func)
    def _wrapper(*args: List, **kwargs: Dict) -> Callable:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err = BaseException("Base Error", "sorry, Unknown Error.")
            res_code = status.HTTP_204_NO_CONTENT
            if isinstance(e, ConnectionRefusedError):
                err = e
                res_code = status.HTTP_405_METHOD_NOT_ALLOWED
            if isinstance(e, PermissionError):
                err = e
                res_code = status.HTTP_401_UNAUTHORIZED
            if isinstance(e, ValidationError):
                err = ValueError(e.detail, "Re-type form data")
                res_code = status.HTTP_400_BAD_REQUEST
            if isinstance(e, AttributeError):
                err = e
                res_code = status.HTTP_400_BAD_REQUEST
            if isinstance(e, ValueError):
                err = e
                res_code = status.HTTP_404_NOT_FOUND
            data = {"alert": err.args[0], "solution": err.args[-1]}
            return Response(data=data, status=res_code)
    return _wrapper


def update(self, request, *args, **kwargs):
    partial = kwargs.pop("partial", False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)

    if getattr(instance, "_prefetched_objects_cache", None):
        instance._prefetched_objects_cache = {}

    return Response(data=None, status=status.HTTP_201_NO_CONTENT)
