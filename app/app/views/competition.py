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
