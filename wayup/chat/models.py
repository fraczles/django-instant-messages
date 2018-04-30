from django.db import models
from django.contrib.auth import get_user_model


class Message(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        get_user_model(),
        related_name="author",
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        get_user_model(),
        related_name="recipient",
        on_delete=models.CASCADE
    )
    body = models.TextField()
