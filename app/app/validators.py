from django.core.exceptions import ValidationError


def greaterThanNegative(value):
    if value < 0:
        raise ValidationError("Value of this integer must be greater than negative!")

def oneOrTwo(value):
    if value != 1 and value != 2:
        raise ValidationError("Value of this integer must be 1 or 2!")
