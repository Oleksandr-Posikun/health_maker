from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from . import models
from .serializers import PersonalDataSerializator


class PersonalDataUserId(APIView):
    def get(self, request, telegram_id, format=None):
        user_data = models.UserPersonalData.objects.filter(telegram_id=telegram_id).first()
        if not user_data:
            return HttpResponseBadRequest()
        ser_word = PersonalDataSerializator(user_data, many=False)

        return Response(ser_word.data)