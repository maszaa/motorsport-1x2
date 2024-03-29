from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class TeamView(APIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=200)

    def put(self, request):
        team = TeamSerializer(data=request.data)
        if team.is_valid():
            team.save()
            response = Response(team.data, status=201)
        else:
            response = Response(team.errors, status=400)
        return response

class SeasonTeamView(APIView):
    def get(self, request):
        try:
            if ("series" and "season") in request.GET:
                series = Series.objects.get(name=request.GET["series"])
                season = series.seasons.get(year=request.GET["season"])
                serializer = SeasonTeamSerializer(season.teams.all(), many=True)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters series and season")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)

    def post(self, request):
        seasonTeam = SeasonTeamSerializer(data=request.data)
        if seasonTeam.is_valid():
            seasonTeam.save()
            response = Response(seasonTeam.data, status=201)
        else:
            response = Response(seasonTeam.errors, status=400)
        return response
