from django.contrib.auth.backends import UserModel
from django.db import models


class User(UserModel):
    id = models.IntegerField(primary_key=True)
    public_key = models.TextField(max_length=100)
    email = models.EmailField()
    password = models.a

