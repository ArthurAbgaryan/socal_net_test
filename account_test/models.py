from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_bithd = models.DateField(null = True, blank=True)

    def __str__(self):
        return 'Profile for user {}',format(self.user.username)