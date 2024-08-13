# Create your models here.
from django.db import models
from django.utils import timezone

from users.models import User


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id')
    stock_code = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return f"Comment by {self.user_id} on {self.stock_code}"