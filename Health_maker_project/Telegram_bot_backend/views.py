import datetime

import pytz
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from Health_maker_project.data_saver import DataSaver
from . import models
from .https_request_security import httpsServerRequestSecurity
from .location_processing import LocationProcessor
from .running_workout_results import RunningWorkoutResults
from .serializers import PersonalDataSerializer


class PersonalDataUserId(APIView):
    security = httpsServerRequestSecurity()

    @csrf_exempt
    def post(self, request, format=None):
        user_state = {'state': 'experienced'}
        if self.security.verify_token(request.headers['Authorization'],
                                      request.headers['user'],
                                      request.headers['user-name']):
            if request.method == 'POST':
                user_data = models.UserPersonalData.objects.filter(telegram_id=request.headers['user']).first()
                if not user_data:
                    new_entry = models.UserPersonalData(telegram_id=request.headers['user'],
                                                        user_name=request.headers['user-name'],
                                                        user_first_name=request.headers['user_first_name'])
                    new_entry.save()
                    user_state['state'] = 'newbie'

                user_personal_information = PersonalDataSerializer(user_data, many=False)

                return Response({'data': user_personal_information.data, 'data_state': user_state})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseForbidden()


class StartRunningWorkouts(APIView):
    security = httpsServerRequestSecurity()
    location_processing = LocationProcessor(models.UsersRunningTrainingData())
    data_saver = DataSaver(models.UsersRunningTrainingData)

    @csrf_exempt
    def post(self, request, format=None):
        if self.security.verify_token(request.headers['Authorization'],
                                      request.headers['User'],
                                      request.headers['User-Position']):
            if request.method == 'POST':
                coordinates = self.location_processing.parse_coordinate(request.headers['User-Position'])
                user_data = models.UserPersonalData.objects.filter(telegram_id=request.headers['User']).first()

                self.data_saver.save_data_in_model(user_id=user_data.id, route_coordinates=[coordinates])

                return Response(status=status.HTTP_200_OK)
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseForbidden()


class RunningWorkoutLasts(APIView):
    security = httpsServerRequestSecurity()
    location_processing = LocationProcessor(models.UsersRunningTrainingData)
    data_saver = DataSaver(models.UsersRunningTrainingData)

    @csrf_exempt
    def post(self, request, format=None):
        if self.security.verify_token(request.headers['Authorization'],
                                      request.headers['User'],
                                      request.headers['User-Position']):
            if request.method == 'POST':
                coordinates = self.location_processing.parse_coordinate(request.headers['User-Position'])
                user_data = models.UserPersonalData.objects.filter(telegram_id=request.headers['User']).first()

                user_training_data = models.UsersRunningTrainingData.objects.filter(user_id=user_data.id,
                                                                                    finish_time=None).first()

                self.data_saver.update_data_in_model(row_id=user_training_data.id,
                                                     row_name='route_coordinates',
                                                     route_coordinates=[coordinates])

                return Response(status=status.HTTP_200_OK)
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseForbidden()


class RunningWorkoutFinish(APIView):
    security = httpsServerRequestSecurity()
    location_processing = LocationProcessor(models.UsersRunningTrainingData)
    data_saver = DataSaver(models.UsersRunningTrainingData)

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

                self.data_saver.overwrite_data(row_id=user_training_data.id,
                                               running_time=time,
                                               route_length=distance,
                                               finish_time=time_now,
                                               route_map=route_map,
                                               user_speed=speed['speed'])

                return Response({'distance': distance, 'time': time, 'speed': speed})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseForbidden()
