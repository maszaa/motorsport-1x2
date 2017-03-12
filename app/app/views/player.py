from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class PlayerView(APIView):
    def get(self, request):
        try:
            if ("serie" and "season" and "competition" and "name") in request.GET:
                serie = Serie.objects.get(name=request.GET["serie"])
                season = serie.seasons.get(year=request.GET["season"])
                competition = season.competitions.get(name=request.GET["competition"])
                player = competition.players.get(name=request.GET["name"])
                serializer = PlayerSerializer(player, many=False)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters serie, season, competition and name")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)

    def post(self, request):
        player = PlayerSerializer(data=request.data)
        if player.is_valid():
            player.save()
            response = Response(player.data, status=201)
        else:
            response = Response(player.errors, status=400)
        return response

class PlayerRowView(APIView):
    def get(self, request):
        try:
            if ("serie" and "season" and "competition" and "name" and "round") in request.GET:
                serie = Serie.objects.get(name=request.GET["serie"])
                season = serie.seasons.get(year=request.GET["season"])
                competition = season.competitions.get(name=request.GET["competition"])
                player = competition.players.get(name=request.GET["name"])
                row = player.rows.filter(roundNumber=request.GET["round"])
                serializer = PlayerRowSerializer(row, many=True)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters serie, season, competition, name and round")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)
