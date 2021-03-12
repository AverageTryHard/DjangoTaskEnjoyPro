import datetime
from django.db import models


class Message(models.Model):
    title: str = models.CharField(max_length=70, blank=False)
    text_body: str = models.CharField(max_length=200, blank=True, default='')
    is_sent: bool = models.BooleanField(default=False)
    is_read: bool = models.BooleanField(default=False)
    created_at: datetime.datetime = models.DateTimeField(auto_now_add=True)
    changed_at: datetime.datetime = models.DateTimeField(auto_now=True)
