from django.contrib import admin
from django.urls import path

from Telegram_bot_backend import views

urlpatterns = [
    path('check_user', views.PersonalDataUserId.as_view()),
    path('start_running_workouts', views.StartRunningWorkouts.as_view()),
    path('running_workouts_lasts', views.RunningWorkoutLasts.as_view()),
    path('running_workouts_finish', views.RunningWorkoutFinish.as_view()),
]
