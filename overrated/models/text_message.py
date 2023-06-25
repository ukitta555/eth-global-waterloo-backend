from django.db import models

from overrated.models import MyUser


class TextMessage(models.Model):
    message_text = models.CharField(max_length=100)
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)


