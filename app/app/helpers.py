from app.models import *


def rowLengthIsCorrect(rowLength, roundId):
    try:
        round_ = Round.objects.get(id=roundId)
        correctRowLength = round_.seasonId.teams.all().count()
        print(correctRowLength, rowLength)
        if rowLength == correctRowLength:
            return True, correctRowLength
        else:
            return False, correctRowLength
    except Round.DoesNotExist as error:
        raise error

def calculatePlayerPoints(playerId, roundId, rowType):
    try:
        player = Player.objects.get(id=playerId)
        roundRow = RoundRow.objects.get(roundId=roundId, rowType=rowType)
        playerRow = PlayerRow.objects.get(playerId=playerId, roundId=roundId, rowType=rowType)
        points = 0

        for roundChar, playerChar in zip(roundRow.row, playerRow.row):
            if roundChar == playerChar:
                if rowType == "Qualifying":
                    points += 1
                elif rowType == "Race":
                    points += 2
        playerRow.pointsFromRow = points
        playerRow.save()

        if rowType == "Qualifying":
            player.qualifyingPoints += points
        elif rowType == "Race":
            player.racePoints += points
        player.save()

        return playerRow
    except Exception as error:
        raise error
