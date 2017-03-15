from django.db import models
from django.core.exceptions import ValidationError
from app.validators import *


class Series(models.Model):
    name = models.CharField(primary_key=True, max_length=64)

class Season(models.Model):
    year = models.IntegerField(null=False, blank=False, validators=[greaterThanNegative])
    series = models.ForeignKey(Series, related_name="seasons", null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("year", "series"))

class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=128)

class SeasonTeam(models.Model):
    team = models.ForeignKey(Team, related_name="seasonsParticipated", null=False, blank=False, on_delete=models.CASCADE)
    seasonId = models.ForeignKey(Season, related_name="teams", null=False, blank=False, on_delete=models.CASCADE)
    runningOrder = models.IntegerField(null=False, blank=False, validators=[greaterThanNegative])

    class Meta:
        ordering = ["runningOrder"]
        unique_together = (("team", "seasonId", "runningOrder"))

class Driver(models.Model):
    name = models.CharField(primary_key=True, max_length=256)

class SeasonDriver(models.Model):
    driver = models.ForeignKey(Driver, related_name="seasonsParticipated", null=False, blank=False, on_delete=models.CASCADE)
    teamId = models.ForeignKey(SeasonTeam, related_name="drivers", null=False, blank=False, on_delete=models.CASCADE)
    carNumber = models.IntegerField(null=False, blank=False, validators=[greaterThanNegative])
    runningOrder = models.IntegerField(null=False, blank=False, validators=[oneOrTwo])

    class Meta:
        ordering = ["runningOrder"]
        unique_together = (("teamId", "driver"))

class Round(models.Model):
    roundNumber = models.IntegerField(null=False, blank=False, validators=[greaterThanNegative])
    roundName = models.CharField(null=False, blank=False, max_length=256)
    seasonId = models.ForeignKey(Season, related_name="rounds", null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("roundNumber", "seasonId"))

class Competition(models.Model):
    seasonId = models.ForeignKey(Season, related_name="competitions", null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=256)

    class Meta:
        unique_together = (("seasonId", "name"))

class Player(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=256)
    qualifyingPoints = models.IntegerField(null=False, blank=False, default=0, validators=[greaterThanNegative])
    racePoints = models.IntegerField(null=False, blank=False, default=0, validators=[greaterThanNegative])
    competitionId = models.ForeignKey(Competition, related_name="players", null=False, blank=False, on_delete=models.CASCADE)

class Row(models.Model):
    QUALIFYING = "Qualifying"
    RACE = "Race"
    ROW_CHOICES = (
        (QUALIFYING, "Qualifying"),
        (RACE, "Race"),
    )

    row = models.CharField(null=False, blank=False, max_length=64)
    rowType = models.CharField(null=False, blank=False, choices=ROW_CHOICES, default=RACE, max_length=1)

    class Meta:
        abstract = True

class RoundRow(Row):
    roundId = models.ForeignKey(Round, related_name="correctRows", null=False, blank=False, on_delete=models.CASCADE)

class PlayerRow(Row):
    playerId = models.ForeignKey(Player, related_name="rows", null=False, blank=False, on_delete=models.CASCADE)
    roundId = models.ForeignKey(Round, related_name="playerRows", null=False, blank=False, on_delete=models.CASCADE)
