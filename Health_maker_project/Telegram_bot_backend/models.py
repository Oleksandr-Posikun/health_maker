from django.db import models

# Create your models here.


class UserPersonalData(models.Model):
    telegram_id = models.CharField(max_length=10, null=False)
    user_first_name = models.CharField(max_length=50, null=False)
    user_name = models.CharField(max_length=50, null=True)
    user_status = models.CharField(max_length=6, null=False, default='user')
    user_active = models.BooleanField(default=True)
    data_time_create = models.DateTimeField(auto_now_add=True)
    data_time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Users personal information's: {self.telegram_id}, First Name: {self.user_first_name}, Active: {self.user_active}"


def user_route_map_upload_path(instance, filename):
    return f'_all_file/user_file/route_maps/' \
           f'{instance.start_time.strftime("%Y")}/' \
           f'{instance.start_time.strftime("%m")}/' \
           f'{instance.start_time.strftime("%d")}/' \
           f'{instance.user.id}/{instance.start_time.strftime("%H_%M_%S")}_map.html'


class UsersRunningTrainingData(models.Model):
    user = models.ForeignKey(UserPersonalData, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    running_time = models.DurationField(null=True, blank=True)
    route_coordinates = models.JSONField(null=True, blank=True)
    route_length = models.FloatField(null=True, blank=True)
    user_speed = models.FloatField(null=True, blank=True)
    route_map = models.FileField(upload_to=user_route_map_upload_path,
                                 null=True, blank=True)

    def __str__(self):
        return f"Users running training: {self.user_id} {self.running_time} {self.route_length}"


