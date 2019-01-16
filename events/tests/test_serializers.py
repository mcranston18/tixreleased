import pytest

from model_mommy import mommy

from events import serializers, models

pytestmark = pytest.mark.django_db


class TestEventSerializer:
    def test_expected_fields(self):
        event = mommy.make("events.Event")
        serializer = serializers.EventSerializer(instance=event)
        assert list(serializer.data.keys()) == [
            "created",
            "id",
            "code",
            "user",
            "status",
        ]


class TestEventHistorySerializer:
    def test_expected_fields(self):
        event_history = mommy.make("events.EventHistory")
        serializer = serializers.EventHistorySerializer(instance=event_history)
        assert list(serializer.data.keys()) == [
            "id",
            "created",
            "response",
            "status",
            "event",
        ]
