from django.db import models
from datetime import datetime, timedelta

def default_registration_deadline():
    return datetime.now() + timedelta(days=2)

class Class(models.Model):
    name = models.CharField(max_length=255)
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    registration_deadline = models.DateTimeField(default=default_registration_deadline)
    date = models.DateField(default=datetime.now)  # 👈 New date field

    def __str__(self):
        return f"{self.name} on {self.date}"
