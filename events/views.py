from rest_framework import generics, viewsets
from rest_framework.response import Response

from . import models, serializers


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer

    def get_queryset(self):
        queryset = models.Event.objects.filter(user=self.request.user)

        return queryset


class EventHistoryViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    serializer_class = serializers.EventHistorySerializer

    def get_queryset(self):
        queryset = models.EventHistory.objects.filter(
            event=self.request.query_params.get("event", None),
            event__user=self.request.user,
        )

        return queryset
