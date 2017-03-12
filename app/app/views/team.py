from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class TeamView(APIView):
    def get(self, request):
        try:
            if "serie" in request.GET:
                serie = Serie.objects.get(name=request.GET["serie"])
                serializer = TeamSerializer(serie.teams.all(), many=True)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters serie")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)

    def put(self, request):
        team = TeamSerializer(data=request.data)
        if team.is_valid():
            team.save()
            response = Response(team.data, status=201)
        else:
            response = Response(team.errors, status=400)
        return response
