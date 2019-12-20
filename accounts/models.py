from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=30, default='', blank=True)
    api_key = models.CharField(max_length=40, default='')
    secret_no = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.user.username



