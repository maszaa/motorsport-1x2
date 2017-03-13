from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class CompetitionView(APIView):
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
            if ("serie" and "season") in request.GET:
                serie = Serie.objects.get(name=request.GET["serie"])
                season = serie.seasons.get(year=request.GET["season"])
                serializer = CompetitionSerializer(season.competitions.all(), many=True)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters serie and season")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)
