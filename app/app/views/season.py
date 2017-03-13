from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class SeasonView(APIView):
    def get(self, request):
        try:
            if "series" in request.GET:
                series = Series.objects.get(name=request.GET["series"])
                serializer = SeasonSerializer(series.seasons.all(), many=True)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters series")
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
