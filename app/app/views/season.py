from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *

class SeasonView(APIView):
    def get(self, request, id):
        try:
            season = Season.objects.get(id=id)
            serializer = SeasonSerializer(season, many=False)
            return Response(serializer.data, status=200)
        except Season.DoesNotExist as error:
            return Response({"Error": str(error)}, status=404)

class SeriesSeasonView(APIView):
    def get(self, request):
        try:
            if "series" in request.GET:
                series = Series.objects.get(name=request.GET["series"])
                serializer = SeasonSerializer(series.seasons.all(), many=True)
                return Response(serializer.data, status=200)
            else:
                seasons = Season.objects.all()
                serializer = SeasonSerializer(seasons, many=True)
                return Response(serializer.data, status=200)
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)

    def post(self, request):
        season = SeasonSerializer(data=request.data)
        if season.is_valid():
            season.save()
            response = Response(season.data, status=201)
        else:
            response = Response(season.errors, status=400)
        return response
