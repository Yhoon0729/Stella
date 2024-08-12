from django.db import models

class Comment(models.Model):
    user_id = models.CharField(max_length=20)
    stock_code = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']