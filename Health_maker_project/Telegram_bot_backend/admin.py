from django.contrib import admin
from . import models


class UserPersonalDataAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'user_first_name', 'user_name', 'user_status', 'user_active', 'data_time_create', 'data_time_update']
    list_editable = ['user_first_name']
    list_display_links = ['telegram_id']


admin.site.register(models.UserPersonalData, UserPersonalDataAdmin)