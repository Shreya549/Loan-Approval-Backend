from django.urls import path, include
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from .views import UserRegistration, UserLogin

urlpatterns = [
    path('register/', UserRegistration.as_view()),
    path('login/', UserLogin.as_view()),
]