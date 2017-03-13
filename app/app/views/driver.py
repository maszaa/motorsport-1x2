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
        drivers = []
        try:
            if ("series" and "season") in request.GET:
                series = Series.objects.get(name=request.GET["series"])
                season = series.seasons.get(year=request.GET["season"])
                teams = season.teams.all()
                for team in teams:
                    teamDrivers = SeasonDriverSerializer(team.drivers.all(), many=True).data
                    for driver in teamDrivers:
                        drivers.append(driver)
                return Response(drivers, status=200)
            else:
                raise KeyError("This query requires parameters series and season")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)

    def post(self, request):
        seasonDriver = SeasonDriverSerializer(data=request.data)
        if seasonDriver.is_valid():
            seasonDriver.save()
            response = Response(seasonDriver.data, status=201)
        else:
            response = Response(seasonDriver.errors, status=400)
        return response
