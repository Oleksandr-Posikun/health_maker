from rest_framework import serializers
from Telegram_bot_backend.models import UserPersonalData
from rest_framework import serializers

class PersonalDataSerializator(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalData
        fields = ['pk', 'telegram_id', ]
