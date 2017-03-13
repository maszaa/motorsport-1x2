from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class DriverView(APIView):
    def get(self, request):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data, status=200)

    def put(self, request):
        driver = DriverSerializer(data=request.data)
        if driver.is_valid():
            driver.save()
            response = Response(driver.data, status=201)
        else:
            response = Response(driver.errors, status=400)
        return response

class SeasonDriverView(APIView):
    def get(self, request):
        return Response()

    def post(self, request):
        seasonDriver = SeasonDriverSerializer(data=request.data)
        if seasonDriver.is_valid():
            seasonDriver.save()
            response = Response(seasonDriver.data, status=201)
        else:
            response = Response(seasonDriver.errors, status=400)
        return response
