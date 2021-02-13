from django.conf import settings
from django.db import models


class Message(models.Model):
    """Messages created by users"""
    content = models.CharField(max_length=160)
    views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Message id: {self.pk}, content: {self.content}'
