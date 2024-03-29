from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, F, IntegerField
from app.models import *
from app.serializers import *
from app.helpers import *


class PlayerView(APIView):
    def get(self, request):
        try:
            if "competitionId" in request.GET:
                competition = Competition.objects.get(id=request.GET["competitionId"])
            elif ("series" and "season" and "competition") in request.GET:
                series = Series.objects.get(name=request.GET["series"])
                season = series.seasons.get(year=request.GET["season"])
                competition = season.competitions.get(name=request.GET["competition"])
            else:
                raise KeyError("This query requires either parameter competitionId or parameters series, season and competition")
            players = competition.players.annotate(points=Sum(F('qualifyingPoints') + F('racePoints'), output_field=IntegerField()))
            serializer = PlayerSerializer(players.order_by("-points", "-racePoints"), many=True)
            return Response(serializer.data, status=200)
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
            if ("series" and "season" and "competition" and "name" and "round") in request.GET:
                series = Series.objects.get(name=request.GET["series"])
                season = series.seasons.get(year=request.GET["season"])
                competition = season.competitions.get(name=request.GET["competition"])
                player = competition.players.get(name=request.GET["name"])
                rows = player.rows.filter(roundNumber=request.GET["round"])
                serializer = PlayerRowSerializer(row, many=True)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters series, season, competition, name and round")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)

    def post(self, request):
        try:
            data = request.data
            data["row"] = cleanRow(data["row"])
            rowIsCorrect, correctRowLength = rowLengthIsCorrect(len(data["row"]), data["round"])
            if rowIsCorrect:
                data["row"] = cleanRow(data["row"])
                playerRow = PlayerRowSerializer(data=data)
                if playerRow.is_valid():
                    playerRow.save()
                    calculatePlayerPoints(data["player"], data["round"], data["rowType"])
                    response = Response(PlayerRowSerializer(PlayerRow.objects.get(player=data["player"], round=data["round"], rowType=data["rowType"]), many=False).data, status=201)
                else:
                    response = Response(playerRow.errors, status=400)
            else:
                response = Response({"error": "Row length is incorrect, it must be " + str(correctRowLength) + "!"}, status=400)
            return response
        except Exception as error:
            return Response({"error": str(error)}, status=400)

class PlayerRowsView(APIView):
    def get(self, request):
        try:
            if ("competitionId" and "roundId") in request.GET:
                rows = PlayerRow.objects.filter(competition=request.GET["competitionId"], round=request.GET["roundId"])
                serializer = PlayerRowSerializer(rows, many=True)
                return Response(serializer.data, status=200)
            else:
                raise KeyError("This query requires parameters competitionId and roundId")
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)
