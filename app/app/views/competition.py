from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class CompetitionView(APIView):
    def get(self, request, id):
        try:
            competition = Competition.objects.get(id=id)
            serializer = CompetitionSerializer(competition, many=False)
            return Response(serializer.data, status=200)
        except Competition.DoesNotExist as error:
            return Response({"Error": str(error)}, status=400)

class CompetitionsView(APIView):
    def get(self, request):
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        competition = CompetitionSerializer(data=request.data)
        if competition.is_valid():
            competition.save()
            response = Response(competition.data, status=201)
        else:
            response = Response(competition.errors, status=400)
        return response

class SeasonCompetitionView(APIView):
    def get(self, request):
        try:
            if ("series" and "season") in request.GET:
                series = Series.objects.get(name=request.GET["series"])
                season = series.seasons.get(year=request.GET["season"])
                serializer = CompetitionSerializer(season.competitions.all(), many=True)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters series and season")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)
