from rest_framework.decorators import (
    api_view,
    throttle_classes,
    authentication_classes,
    permission_classes,
    renderer_classes,
    schema,
    action
)
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
from accounts.serializers import UserDetailSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
import json
import logging
from config.utils import response_error_handler
@permission_classes([permissions.AllowAny])
@api_view(["GET", "POST"])
@response_error_handler
def get_user_view(request:Request) -> Response:
    """[summary]

    Arguments:
        request {Request} -- [description]
    
    Schma:
        GET:
        
        POST:

    Raises:
        PermissionError: [description]
        ConnectionRefusedError: [description]
    
    Returns:
        Response -- [description]
    """
    serializer:Serializer
    if request.method == "GET":
        queryset = get_user_model().objects.all()
        serializer =UserDetailSerializer(queryset, many=True)
        raise PermissionError("error", "try Get or post") 
        return Response(serializer.data)
    if request.method == "POST":
        serializer = UserCreateSerializer(data=request.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    raise ConnectionRefusedError()
    # return Response("not allowed method", status=status.HTTP_405_METHOD_NOT_ALLOWED)
# @permission_classes([permissions.AllowAny])
# @api_view(["POST"])
# def post_user_view(req:request.Request) -> response.Response:
    # 