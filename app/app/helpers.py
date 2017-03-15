from app.models import *


def rowLengthIsCorrect(rowLength, roundId):
    round_ = Round.objects.get(id=roundId)
    correctRowLength = round_.seasonId.teams.all().count()
    print(correctRowLength, rowLength)
    if rowLength == correctRowLength:
        return True, correctRowLength
    else:
        return False, correctRowLength
