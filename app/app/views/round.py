from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *
from parsers.onextwo import *

class RoundView(APIView):
    def get(self, request, id):
        try:
            round_ = Round.objects.get(id=id)
            serializer = RoundSerializer(round_, many=False)
            return Response(serializer.data, status=200)
        except Round.DoesNotExist as error:
            return Response({"Error": str(error)}, status=400)

class RoundsView(APIView):
    def get(self, request):
        try:
            if "seasonId" in request.GET:
                rounds = Round.objects.filter(season=request.GET["seasonId"])
            elif ("series" and "season") in request.GET:
                series = Series.objects.get(name=request.GET["series"])
                season = series.seasons.get(year=request.GET["season"])
                rounds = season.rounds.all()
            else:
                raise KeyError("This query requires either parameter seasonId or parameters series and season (year)")
            serializer = RoundSerializer(rounds, many=True)
            return Response(serializer.data, status=200)
        except KeyError as error:
            return Response({"Error": str(error)}, status=400)
        except Exception as error:
            return Response({"Error": str(error)}, status=404)

    def post(self, request):
        data = request.data
        try:
            series = Series.objects.get(name=data["series"])
            season = series.seasons.get(year=data["season"])
            teamsDrivers = SeasonTeamSerializer(season.teams.all(), many=True).data
            rowParser = OneXTwo(data["series"], data["season"], data["round"], teamsDrivers)

            roundData = {"season": season.id, "roundNumber": data["round"], "roundName": rowParser.getRoundName()}

            roundSerializer = RoundSerializer(data=roundData)
            if roundSerializer.is_valid():
                roundSerializer.save()
            else:
                return Response(roundSerializer.errors, status=400)

            qualifyingRow = rowParser.getQualifyingRow()
            raceRow = rowParser.getRaceRow()

            qualifyingRowData = {"row": qualifyingRow, "rowType": Row.QUALIFYING, "round": roundSerializer.data["id"]}
            qualifyingRowSerializer = RoundRowSerializer(data=qualifyingRowData)
            if qualifyingRowSerializer.is_valid():
                qualifyingRowSerializer.save()
            else:
                return Response(qualifyingRowSerializer.errors, status=400)

            raceRowData = {"row": raceRow, "rowType": Row.RACE, "round": roundSerializer.data["id"]}
            raceRowSerializer = RoundRowSerializer(data=raceRowData)
            if raceRowSerializer.is_valid():
                raceRowSerializer.save()
            else:
                return Response(raceRowSerializer.errors, status=400)

            return Response(RoundSerializer(Round.objects.get(id=roundSerializer.data["id"])).data, status=201)
        except Exception as error:
            return Response({"error": str(error)}, status=400)
