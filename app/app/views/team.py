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
        return Response()

    def post(self, request):
        seasonTeam = SeasonTeamSerializer(data=request.data)
        if seasonTeam.is_valid():
            seasonTeam.save()
            response = Response(seasonTeam.data, status=201)
        else:
            response = Response(seasonTeam.errors, status=400)
        return response
