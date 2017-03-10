from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.core.exceptions import ValidationError
from app.models import Player
from app.serializers import *


class PlayerInfo(APIView):
    def get(self, request, id):
        try:
            player = Player.objects.get(id=id)
            serializer = PlayerSerializer(player, many=False)
            response = Response(serializer.data, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            response = Response({"Error": "Player with id " + id + " was not found"}, status=status.HTTP_404_NOT_FOUND)
        return response


class AddPlayer(APIView):
    def get(self, request):
        return Response()

    @csrf_exempt
    def post(self, request):
        player = PlayerSerializer(data=request.data)
        if player.is_valid():
            player.save()
            response = Response(player.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(player.errors, status=status.HTTP_404_NOT_FOUND)
        return response
