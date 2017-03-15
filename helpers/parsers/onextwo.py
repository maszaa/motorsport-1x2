from ergastquerier import *


class OneXTwo(ErgastQuerier):
    def __init__(self, series, season, roundNumber, teamsDrivers):
        super(OneXTwo, self).__init__(series, season, roundNumber)

        self.__teamsDrivers = teamsDrivers

        self.__qualifyingResults = {result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]: result \
            for result in super(OneXTwo, self).getQualifyingResults()}
        self.__raceResults = {result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]: result \
            for result in super(OneXTwo, self).getRaceResults()}

        self.__raceLaps = int(super(OneXTwo, self).getRaceResults()[0]["laps"])
        self.__qualifyingRow = self.__parseQualifyingRow()
        self.__raceRow = self.__parseRaceRow()

    def __parseQualifyingRow(self):
        qualifyingRow = ""
        for team in self.__teamsDrivers:
            driverPositions = {}
            for driver in team["drivers"]:
                try:
                    driverPositions[str(driver["runningOrder"])] = int(self.__qualifyingResults[driver["driver"]]["position"])
                except KeyError:
                    continue

            if ("1" and "2") not in driverPositions:
                qualifyingRow += "X"
            elif "1" not in driverPositions:
                qualifyingRow += "2"
            elif "2" not in driverPositions:
                qualifyingRow += "1"
            elif (driverPositions["1"] == driverPositions["2"] + 1) or (driverPositions["2"] == driverPositions["1"] + 1):
                qualifyingRow += "X"
            elif driverPositions["1"] < driverPositions["2"] - 1:
                qualifyingRow += "1"
            elif driverPositions["2"] < driverPositions["1"] - 1:
                qualifyingRow += "2"

        if len(qualifyingRow) == len(self.__teamsDrivers):
            return qualifyingRow
        else:
            raise ErgastQuerierException("qualifying row doesn't match the amount of teams!")

    def __parseRaceRow(self):
        raceRow = ""
        for team in self.__teamsDrivers:
            driverPositions = {}
            for driver in team["drivers"]:
                try:
                    driverPositions[str(driver["runningOrder"])] = {"position": int(self.__raceResults[driver["driver"]]["position"]), \
                                                                    "positionStatus": self.__raceResults[driver["driver"]]["positionText"], \
                                                                    "laps": int(self.__raceResults[driver["driver"]]["laps"])}
                except KeyError:
                    continue

            if ("1" and "2") not in driverPositions:
                raceRow += "X"
            elif "1" not in driverPositions:
                raceRow += "2"
            elif "2" not in driverPositions:
                raceRow += "1"
            elif not (driverPositions["1"]["positionStatus"]).isdigit() and not (driverPositions["2"]["positionStatus"]).isdigit():
                raceRow += "X"
            elif driverPositions["1"]["position"] == driverPositions["2"]["position"] + 1:
                if (driverPositions["1"]["laps"] / self.__raceLaps > 0.9 and (driverPositions["1"]["positionStatus"]).isdigit()):
                    raceRow += "X"
                else:
                    raceRow += "2"
            elif driverPositions["2"]["position"] == driverPositions["1"]["position"] + 1:
                if (driverPositions["2"]["laps"] / self.__raceLaps > 0.9 and (driverPositions["2"]["positionStatus"]).isdigit()):
                    raceRow += "X"
                else:
                    raceRow += "1"
            elif driverPositions["1"]["position"] < driverPositions["2"]["position"] - 1:
                raceRow += "1"
            elif driverPositions["2"]["position"] < driverPositions["1"]["position"] - 1:
                raceRow += "2"

        if len(raceRow) == len(self.__teamsDrivers):
            return raceRow
        else:
            raise ErgastQuerierException("Race row doesn't match the amount of teams!")

    def getQualifyingRow(self):
        return self.__qualifyingRow

    def getRaceRow(self):
        return self.__raceRow
