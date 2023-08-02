from rest_framework import serializers
from Telegram_bot_backend.models import UserPersonalData, UsersRunningTrainingData


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalData
        fields = ['pk', 'telegram_id']


class RunningTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersRunningTrainingData
        fields = ['pk']
