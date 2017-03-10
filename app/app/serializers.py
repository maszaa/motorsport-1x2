from rest_framework import serializers
from app.models import *


class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = ("name")

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ("id", "year", "serie")

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("name")

class SeasonTeamSerializer(TeamSerializer):
    class Meta:
        model = SeasonTeam
        fields = ("id", "season", "runningOrder")

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("name", "carNumber")

class SeasonDriverSerializer(DriverSerializer):
    class Meta:
        model = SeasonDriver
        fields = ("id", "team", "runningOrder")

class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ("id", "roundNumber", "roundName", "season")

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ("id", "season", "name")

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("id", "name", "qualificationPoints", "racePoints", "competition")

class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ("id", "row", "rowtype")

class RoundRowSerializer(RowSerializer):
    class Meta:
        model = RoundRow
        fields = ("id", "roundNumber")

class PlayerRowSerializer(RowSerializer):
    class Meta:
        model = PlayerRow
        fields = ("id", "player")
