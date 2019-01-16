from django.contrib.auth.models import AbstractUser
from django.db import models

from tixreleased.models import BaseModel


class CustomUser(AbstractUser, BaseModel):
    pass
