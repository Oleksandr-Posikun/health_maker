import re

from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .https_request_security import httpsServerRequestSecurity
from .serializers import PersonalDataSerializer, ResponseSerializer


class PersonalDataUserId(APIView):
    security = httpsServerRequestSecurity()

    def get(self, request, token, telegram_id, user_name, user_first_name, format=None):
        user_state = {'state': 'experienced'}

        if self.security.verify_token(token, telegram_id, user_name, user_first_name):
            user_data = models.UserPersonalData.objects.filter(telegram_id=telegram_id).first()

            if not user_data:
                new_entry = models.UserPersonalData(telegram_id=telegram_id,
                                                    user_name=user_name,
                                                    user_first_name=user_first_name)
                new_entry.save()
                user_state['state'] = 'newbie'

            user_personal_information = PersonalDataSerializer(user_data, many=False)

            return Response({'data': user_personal_information.data, 'data_state': user_state})
        else:
            return HttpResponseBadRequest()


class RunningWorkouts(APIView):
    security = httpsServerRequestSecurity()

    @csrf_exempt
    def post(self, request, format=None):
        if self.security.verify_token(request.headers['Authorization'],
                                      request.headers['User'],
                                      request.headers['User-Position']):
            if request.method == 'POST':

                info = request.headers
                coordinates = self.create_coordinate(info['User-Position'])
                user_data = models.UserPersonalData.objects.filter(telegram_id=info['User']).first()

                self.save_data_in_model(models.UsersRunningTrainingData,
                                        user_id=user_data.id,
                                        route_coordinates=coordinates)

                serializer = ResponseSerializer(data={'data': 'you win'})
                serializer.is_valid(raise_exception=True)

                return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response({'data': 'error'})

    def create_coordinate(self, coordinate):
        data = coordinate
        pattern = r'\d+\.\d+'
        matches = re.findall(pattern, data)

        numbers = [float(match) for match in matches]

        return numbers

    def save_data_in_model(self, model, **kwargs):
        new = model(kwargs)
        new.save()

    def update_data_in_model(self):
        pass
