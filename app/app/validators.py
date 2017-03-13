from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
from app.models import *


def greaterThanZero(value):
    if value <= 0:
        raise ValidationError("Value of this integer must be greater than zero!")

def rowLengthIsCorrect(value):
    rowLength = Season.teams.all().count()
    if value != rowLength:
        raise ValidationError(
            ugettext_lazy("Row length was incorrect, it must be %(value)s!"),
            params={'value': rowLength})

def oneOrTwo(value):
    if value != 1 and value != 2:
        raise ValidationError("Value of this integer must be 1 or 2!")
