from django.conf import settings
import jwt, requests, uuid
from .models import User
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework import viewsets, permissions, generics
from .serializers import UserRegistrationSerializer, UserLoginSerializer
import uuid, os, base64
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.template.loader import render_to_string
from datetime import datetime, timezone
# Create your views here.

class UserRegistration(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        # print('hi')
        serializer = self.serializer_class(data=request.data)
        # print(serializer)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



