from ergastquerier import *


class OneXTwo(ErgastQuerier):
    def __init__(self, series, season, roundNumber, teamsDrivers):
        super(OneXTwo, self).__init__(series, season, roundNumber)

        self.__teamsDrivers = teamsDrivers

        self.__qualificationResults = {result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]: result \
            for result in super(OneXTwo, self).getQualificationResults()}
        self.__raceResults = {result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]: result \
            for result in super(OneXTwo, self).getRaceResults()}

        self.__qualificationRow = ""
        self.__raceRow = ""
        self.__parseQualificationRow()
        self.__parseRaceRow()

    def __parseQualificationRow(self):
        for team in self.__teamsDrivers:
            driverPositions = {}
            for driver in team["drivers"]:
                try:
                    driverPositions[str(driver["runningOrder"])] = int(self.__qualificationResults[driver["driver"]]["position"])
                except KeyError:
                    continue

            if ("1" and "2") not in driverPositions:
                self.__qualificationRow += "X"
            elif "1" not in driverPositions:
                self.__qualificationRow += "2"
            elif "2" not in driverPositions:
                self.__qualificationRow += "1"
            elif (driverPositions["1"] == driverPositions["2"] + 1) or (driverPositions["2"] == driverPositions["1"] + 1):
                self.__qualificationRow += "X"
            elif driverPositions["1"] < driverPositions["2"] - 1:
                self.__qualificationRow += "1"
            elif driverPositions["2"] < driverPositions["1"] - 1:
                self.__qualificationRow += "2"

    def __parseRaceRow(self):
        return ""

    def getQualificationRow(self):
        return self.__qualificationRow

    def getRaceRow(self):
        return "XXXXXXXXXXX"
        return self.__raceRow
