from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *


class SeriesView(APIView):
    def get(self, request):
        series = Series.objects.all()
        serializer = SeriesSerializer(series, many=True)
        return Response(serializer.data, status=200)

    def put(self, request):
        series = SeriesSerializer(data=request.data)
        if series.is_valid():
            series.save()
            response = Response(series.data, status=201)
        else:
            response = Response(series.errors, status=400)
        return response
