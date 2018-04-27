from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        'auth.User',
        related_name="sender",
        on_delete=models.CASCADE
    )
    reciever = models.ForeignKey(
        'auth.User',
        related_name="reciever",
        on_delete=models.CASCADE
    )
    body = models.TextField()
