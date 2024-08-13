from django.db import models
from django.utils import timezone

class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100, unique=True)
    user_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    gender = models.IntegerField(default=0)
    reset_password_token = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.user_id