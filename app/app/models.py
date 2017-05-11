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

    def __str__(self):
        return '%d' % (self.year)

class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=128)

class SeasonTeam(models.Model):
    team = models.ForeignKey(Team, related_name="seasonsParticipated", null=False, blank=False, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, related_name="teams", null=False, blank=False, on_delete=models.CASCADE)
    runningOrder = models.IntegerField(null=False, blank=False, validators=[greaterThanNegative])

    class Meta:
        ordering = ["runningOrder"]
        unique_together = (("team", "season", "runningOrder"))

    def __str__(self):
        return '%d. %s' % (self.runningOrder, self.team.name)

class Driver(models.Model):
    name = models.CharField(primary_key=True, max_length=256)

class SeasonDriver(models.Model):
    driver = models.ForeignKey(Driver, related_name="seasonsParticipated", null=False, blank=False, on_delete=models.CASCADE)
    team = models.ForeignKey(SeasonTeam, related_name="drivers", null=False, blank=False, on_delete=models.CASCADE)
    carNumber = models.IntegerField(null=False, blank=False, validators=[greaterThanNegative])
    runningOrder = models.IntegerField(null=False, blank=False, validators=[oneOrTwo])

    class Meta:
        ordering = ["runningOrder"]
        unique_together = (("team", "driver"))

    def __str__(self):
        return '%s' % (self.driver.name)

class Round(models.Model):
    roundNumber = models.IntegerField(null=False, blank=False, validators=[greaterThanNegative])
    roundName = models.CharField(null=False, blank=False, max_length=256)
    season = models.ForeignKey(Season, related_name="rounds", null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("roundNumber", "season"))

    def __str__(self):
        return '%d. %s' % (self.roundNumber, self.roundName)

class Competition(models.Model):
    season = models.ForeignKey(Season, related_name="competitions", null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=256)

    class Meta:
        unique_together = (("season", "name"))

    def __str__(self):
        return '%s' % (self.name)

class Player(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=256)
    qualifyingPoints = models.IntegerField(null=False, blank=False, default=0, validators=[greaterThanNegative])
    racePoints = models.IntegerField(null=False, blank=False, default=0, validators=[greaterThanNegative])
    competition = models.ForeignKey(Competition, related_name="players", null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.name)

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
    round = models.ForeignKey(Round, related_name="correctRows", null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("round", "rowType"))

    def __str__(self):
        return '%d, %s: %s' % (self.round.roundNumber, self.rowType, self.row)

class PlayerRow(Row):
    player = models.ForeignKey(Player, related_name="rows", null=False, blank=False, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name="rows", null=False, blank=False, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, related_name="playerRows", null=False, blank=False, on_delete=models.CASCADE)
    pointsFromRow = models.IntegerField(null=False, blank=False, validators=[greaterThanNegative], default=0)

    class Meta:
        unique_together = (("player", "round", "rowType"))

    def __str__(self):
        return '%d;%s;%s' % (self.round.roundNumber, self.rowType, self.row)
