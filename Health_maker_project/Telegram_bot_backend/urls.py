from django.contrib import admin
from django.urls import path

from Telegram_bot_backend import views

urlpatterns = [
    path('<token>/<telegram_id>/<user_name>/<user_first_name>', views.PersonalDataUserId.as_view()),
    path('running_workouts', views.RunningWorkouts.as_view()),
]
