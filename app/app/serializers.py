from rest_framework import serializers
from app.models import *


class CompetitionSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Round
        fields = "__all__"

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"

class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = "__all__"

class PlayerRowSerializer(RowSerializer):
    class Meta:
        model = PlayerRow
        fields = "__all__"
