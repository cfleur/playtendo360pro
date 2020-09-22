from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10,
                                    choices=(('player','Player'),('developer','Developer')))
    account_balance = models.FloatField(default=0)
    avatar = models.ImageField(upload_to='profile_avatar', blank=False, default='staticfiles/default_avatar.png')
