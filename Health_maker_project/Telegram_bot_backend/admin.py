from django.contrib import admin
from .models import UsersRunningTrainingData, UserPersonalData


class UserPersonalDataAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'user_first_name', 'user_name', 'user_status', 'user_active', 'data_time_create', 'data_time_update']
    list_editable = ['user_first_name']
    list_display_links = ['telegram_id']


admin.site.register(UserPersonalData, UserPersonalDataAdmin)


class UsersRunningTrainingDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'start_time', 'finish_time', 'running_time', 'route_coordinates', 'route_length')
    list_filter = ('user_id', 'start_time', 'finish_time')
    search_fields = ('user_id__username', 'route_coordinates')


admin.site.register(UsersRunningTrainingData, UsersRunningTrainingDataAdmin)
