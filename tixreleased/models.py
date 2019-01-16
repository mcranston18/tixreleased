import uuid

from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
