from rest_framework import serializers
from django.db.models import Sum, F, IntegerField
from app.models import *


class RoundRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundRow
        fields = "__all__"

class PlayerRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRow
        fields = "__all__"

class PlayerSerializer(serializers.ModelSerializer):
    rows = PlayerRowSerializer(many=True, read_only=True)
    points = serializers.IntegerField()

    class Meta:
        model = Player
        fields = "__all__"

class CompetitionSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Competition
        fields = "__all__"

class SeasonDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonDriver
        fields = "__all__"

class SeasonTeamSerializer(serializers.ModelSerializer):
    drivers = SeasonDriverSerializer(many=True, read_only=True)

    class Meta:
        model = SeasonTeam
        fields = "__all__"

class SeasonSerializer(serializers.ModelSerializer):
    competitions = CompetitionSerializer(many=True, read_only=True)
    teams = SeasonTeamSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = "__all__"

class SeriesSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"

class RoundSerializer(serializers.ModelSerializer):
    correctRows = RoundRowSerializer(many=True, read_only=True)
    playerRows = RoundRowSerializer(many=True, read_only=True)

    class Meta:
        model = Round
        fields = "__all__"
