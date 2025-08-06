from django.db import models
from django.utils import timezone


class Greeting(models.Model):
    message = models.CharField(max_length=200, default="Hello, World!")
    created_at = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.message} (count: {self.count})"

    class Meta:
        ordering = ["-created_at"]
