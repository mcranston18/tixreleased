from rest_framework import serializers

from users.serializers import UserSerializer
from . import models


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Event
        fields = ["created", "id", "code", "user", "status"]
        ordering = "-created"


class EventHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventHistory
        fields = ["id", "created", "response", "status", "event"]
        ordering = "-created"
