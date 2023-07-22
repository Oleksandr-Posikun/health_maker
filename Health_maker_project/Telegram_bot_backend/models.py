from django.db import models

# Create your models here.


class UserPersonalData(models.Model):
    telegram_id = models.CharField(max_length=10, null=False)
    user_first_name = models.CharField(max_length=50, null=False)
    user_name = models.CharField(max_length=50, null=True)
    user_status = models.CharField(max_length=6, null=False, default='user')
    user_active = models.BooleanField(default=False)
    data_time_create = models.DateTimeField(auto_now_add=True)
    data_time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Telegram ID: {self.telegram_id}, First Name: {self.user_first_name}, Active: {self.user_active}"
