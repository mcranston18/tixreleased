from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
