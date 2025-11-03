from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_tokens")
    access_token = models.CharField(max_length=400)
    refresh_token = models.CharField(max_length=400)
    expire_in_timestamp = models.IntegerField()

    class Meta:
        db_table = 'auth_user_token'
        ordering = ("id",)
