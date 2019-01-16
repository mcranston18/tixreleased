from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets

from . import serializers

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
