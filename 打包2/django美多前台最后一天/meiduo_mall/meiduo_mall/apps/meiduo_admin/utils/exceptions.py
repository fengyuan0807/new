from django.db import DatabaseError
from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        if isinstance(exc, DatabaseError):
            return Response({'detail': '数据库错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    return response
