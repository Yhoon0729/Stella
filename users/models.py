from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100)
    user_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'users'  # 실제 DB 테이블 이름을 지정

    def __str__(self):
        return self.user_id