import datetime

import pytz
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .https_request_security import httpsServerRequestSecurity
from .location_processing import LocationProcessing, RunningWorkoutResults
from .serializers import PersonalDataSerializer, RunningTrainingSerializer


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


class StartRunningWorkouts(APIView):
    security = httpsServerRequestSecurity()
    location_processing = LocationProcessing(models.UsersRunningTrainingData)

    @csrf_exempt
    def post(self, request, format=None):
        if self.security.verify_token(request.headers['Authorization'],
                                      request.headers['User'],
                                      request.headers['User-Position']):
            if request.method == 'POST':
                coordinates = self.location_processing.process_coordinate(request.headers['User-Position'])
                user_data = models.UserPersonalData.objects.filter(telegram_id=request.headers['User']).first()

                self.location_processing.save_data(user_id=user_data.id, route_coordinates=[coordinates])

                return Response(status=status.HTTP_200_OK)
        else:
            return Response({'data': 'error'})


class RunningWorkoutLasts(APIView):
    security = httpsServerRequestSecurity()
    location_processing = LocationProcessing(models.UsersRunningTrainingData)

    @csrf_exempt
    def post(self, request, format=None):
        if self.security.verify_token(request.headers['Authorization'],
                                      request.headers['User'],
                                      request.headers['User-Position']):
            if request.method == 'POST':
                coordinates = self.location_processing.process_coordinate(request.headers['User-Position'])
                user_data = models.UserPersonalData.objects.filter(telegram_id=request.headers['User']).first()

                user_training_data = models.UsersRunningTrainingData.objects.filter(user_id=user_data.id,
                                                                                    finish_time=None).first()

                self.location_processing.update_data(row_id=user_training_data.id,
                                                     row_name='route_coordinates',
                                                     route_coordinates=[coordinates])

                return Response(status=status.HTTP_200_OK)
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class RunningWorkoutFinish(APIView):
    security = httpsServerRequestSecurity()
    location_processing = LocationProcessing(models.UsersRunningTrainingData)

    @csrf_exempt
    def post(self, request, format=None):
        if self.security.verify_token(request.headers['Authorization'],
                                      request.headers['User'],
                                      request.headers['finish_time']):
            if request.method == 'POST':
                user_data = models.UserPersonalData.objects.filter(telegram_id=request.headers['User']).first()
                user_training_data = models.UsersRunningTrainingData.objects.filter(user_id=user_data.id,
                                                                                    finish_time=None).first()
                time_now = datetime.datetime.now()
                utc_zone = pytz.timezone('UTC')
                time_now = time_now.astimezone(utc_zone)

                result = RunningWorkoutResults(user_training_data.start_time,
                                               time_now,
                                               user_training_data.route_coordinates)

                time = result.get_run_time()
                distance = result.get_distance()
                route_map = result.get_map()
                speed = result.get_speed()

                self.location_processing.overwrite_data(row_id=user_training_data.id,
                                                        running_time=time,
                                                        route_length=distance,
                                                        finish_time=time_now,
                                                        route_map=route_map,
                                                        user_speed=speed['speed'])

                return Response({'distance': distance, 'time': time, 'speed': speed})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
