import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    token = models.CharField(max_length=32, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    cash = models.PositiveSmallIntegerField(default=10000)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        if not self.token:
            self.token = str(uuid.uuid4()).replace('-', '')
        return super(User, self).save(*args, **kwargs)
