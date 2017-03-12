from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class SerieView(APIView):
    def get(self, request):
        series = Serie.objects.all()
        serializer = SerieSerializer(series, many=True)
        return Response(serializer.data, status=200)

    def put(self, request):
        serie = SerieSerializer(data=request.data)
        if serie.is_valid():
            serie.save()
            response = Response(serie.data, status=201)
        else:
            response = Response(serie.errors, status=400)
        return response
