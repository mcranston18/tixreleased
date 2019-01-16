from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField

from tixreleased.models import BaseModel
from .ticket_finder import TicketFinder


class EventHistory(BaseModel):
    SUCCESS = "success"
    ERROR = "error"
    STATUS_CHOICES = ((SUCCESS, "success"), (ERROR, "error"))

    response = JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    event = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, related_name="event_history"
    )


class Event(BaseModel):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    STATUS_CHOICES = ((ACTIVE, "Active"), (INACTIVE, "Inactive"), (ERROR, "Error"))

    code = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=INACTIVE)

    class Meta:
        unique_together = ("code", "user")

    def save(self, *args, **kwargs):
        tickets = TicketFinder(event_id=self.code).get_availability()

        if tickets.get("error"):
            self.status = Event.ERROR
        else:
            self.status = Event.ACTIVE

        super(Event, self).save(*args, **kwargs)

        EventHistory.objects.create(
            event_id=self.id,
            response=tickets,
            status="error" if tickets.get("error") else "success",
        )

    def __str__(self):
        return self.code
