import pytest
from unittest.mock import MagicMock

from django.urls import reverse
from model_mommy import mommy

from events import models, views, serializers

pytestmark = pytest.mark.django_db


@pytest.fixture
def logged_in_client(client):
    user = mommy.make("users.CustomUser")
    client.user = user
    client.force_login(user=user)
    return client


@pytest.fixture
def create_events(logged_in_client):
    return [
        mommy.make("events.Event", user=logged_in_client.user),
        mommy.make("events.Event"),
    ]


@pytest.fixture
def create_event_histories(create_events):
    return [
        mommy.make("events.EventHistory", event=create_events[0]),
        mommy.make("events.EventHistory", event=create_events[1]),
    ]


class TestEventViewSet:
    def test_serializer_class(self):
        assert (
            views.EventViewSet().get_serializer_class() == serializers.EventSerializer
        )

    def test_get_queryset(self, logged_in_client, create_events):
        """
        Test get_queryset only returns objects owned by request.user
        """
        user = logged_in_client.user

        expected_events = models.Event.objects.filter(user=user)
        queryset = views.EventViewSet(request=MagicMock(user=user)).get_queryset()

        assert models.Event.objects.count() > 1
        assert len(queryset) == 1
        assert [x.id for x in queryset] == [x.id for x in expected_events]


class TestEventsListView:
    url = reverse("event-list")

    def test_without_authentication(self, client):
        response = client.get(self.url)
        assert response.status_code == 403

    def test_with_authentication(self, logged_in_client):
        response = logged_in_client.get(self.url)
        assert response.status_code == 200


class TestEventsDetailView:
    url = reverse("event-list")
    get_url = lambda self, x: reverse("event-detail", kwargs={"pk": x.id})

    def test_get_detail_by_owner(self, logged_in_client, create_events):
        event = next(
            (x for x in create_events if logged_in_client.user == x.user), None
        )
        response = logged_in_client.get(self.get_url(event))
        assert response.status_code == 200
        assert response.json().get("id") == str(event.id)

    def test_get_detail_by_stranger(self, logged_in_client, create_events):
        event = next(
            (x for x in create_events if logged_in_client.user != x.user), None
        )
        response = logged_in_client.get(self.get_url(event))
        assert response.status_code == 404


class TestEventHistoryViewSet:
    url = reverse("event-history-list")

    def test_serializer_class(self):
        assert (
            views.EventHistoryViewSet().get_serializer_class()
            == serializers.EventHistorySerializer
        )

    def test_without_authentication(self, client):
        response = client.get(self.url)
        assert response.status_code == 403

    def test_list_returns_by_event(self, logged_in_client, create_event_histories):
        """
        Test that the event-history-list only returns the history of one event owned by the user
        """
        sample_event = models.Event.objects.filter(
            event_history__isnull=False, user=logged_in_client.user
        ).first()

        event_id = str(sample_event.id)
        response = logged_in_client.get(f"{self.url}?event={event_id}")
        assert response.status_code == 200
        assert all(x["event"] == event_id for x in response.json())

    def test_get_list_by_stranger(self, logged_in_client, create_event_histories):
        """
        Test that non-owner cannot fetch event history of another user's event
        """
        sample_event = (
            models.Event.objects.exclude(user=logged_in_client.user)
            .filter(event_history__isnull=False)
            .first()
        )
        event_id = str(sample_event.id)
        response = logged_in_client.get(f"{self.url}?event={event_id}")
        assert response.status_code == 200
        assert not response.json()
