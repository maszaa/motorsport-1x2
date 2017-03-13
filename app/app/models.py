from django.db import models
from django.core.exceptions import ValidationError
from app.validators import *


class Serie(models.Model):
    name = models.CharField(primary_key=True, max_length=64)

class Season(models.Model):
    year = models.IntegerField(null=False, blank=False, validators=[greaterThanZero])
    serie = models.ForeignKey(Serie, related_name="seasons", null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("year", "serie"))

class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=128)
    serie = models.ForeignKey(Serie, related_name="teams", null=False, blank=False, on_delete=models.CASCADE)

class SeasonTeam(models.Model):
    team = models.ForeignKey(Team, related_name="seasonsParticipated", null=False, blank=False, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, related_name="teams", null=False, blank=False, on_delete=models.CASCADE)
    runningOrder = models.IntegerField(primary_key=True, validators=[greaterThanZero])

    class Meta:
        unique_together = (("team", "season", "runningOrder"))

class Driver(models.Model):
    name = models.CharField(primary_key=True, max_length=256)
    carNumber = models.IntegerField(validators=[greaterThanZero])
    serie = models.ForeignKey(Serie, related_name="drivers", null=False, blank=False, on_delete=models.CASCADE)

class SeasonDriver(models.Model):
    driver = models.ForeignKey(Driver, related_name="seasonsParticipated", null=False, blank=False, on_delete=models.CASCADE)
    team = models.ForeignKey(SeasonTeam, related_name="drivers", null=False, blank=False, on_delete=models.CASCADE)
    runningOrder = models.IntegerField(null=False, blank=False, validators=[oneOrTwo])

    class Meta:
        unique_together = (("team", "driver", "runningOrder"))

class Round(models.Model):
    roundNumber = models.IntegerField(null=False, blank=False, validators=[greaterThanZero])
    roundName = models.CharField(null=False, blank=False, max_length=256)
    season = models.ForeignKey(Season, related_name="rounds", null=False, blank=False, on_delete=models.CASCADE)

class Competition(models.Model):
    season = models.ForeignKey(Season, related_name="competitions", null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=256)

    class Meta:
        unique_together = (("season", "name"))

class Player(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=256)
    qualificationPoints = models.IntegerField(null=False, blank=False, default=0, validators=[greaterThanZero])
    racePoints = models.IntegerField(null=False, blank=False, default=0, validators=[greaterThanZero])
    competition = models.ForeignKey(Competition, related_name="players", null=False, blank=False, on_delete=models.CASCADE)

class Row(models.Model):
    QUALIFICATION = "Q"
    RACE = "R"
    ROW_CHOICES = (
        (QUALIFICATION, "qualification"),
        (RACE, "race"),
    )

    row = models.CharField(null=False, blank=False, validators=[rowLengthIsCorrect], max_length=64)
    rowType = models.CharField(null=False, blank=False, choices = ROW_CHOICES, default=RACE, max_length=1)
    roundNumber = models.ForeignKey(Round, related_name="rows", null=False, blank=False, on_delete=models.CASCADE)

class PlayerRow(Row):
    player = models.ForeignKey(Player, related_name="rows", null=False, blank=False, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name="rows", null=False, blank=False, on_delete=models.CASCADE)
