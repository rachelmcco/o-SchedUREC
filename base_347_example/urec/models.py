from django.db import models
from datetime import datetime, timedelta

# Define the default function *before* using it
def default_registration_deadline():
    return datetime.now() + timedelta(hours=48)

class Class(models.Model):
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    date = models.DateField()
    registration_deadline = models.DateTimeField(default=default_registration_deadline)

    def __str__(self):
        return f"{self.name} on {self.date}"

from django.conf import settings  # needed for the User model

class SavedClass(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    urec_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} saved {self.urec_class.name}"
