import requests
from ergastquerier import *


class OneXTwo(ErgastQuerier):
    def __init__(self, series, season, roundNumber, teamsDrivers):
        super(OneXTwo, self).__init__(series, season, roundNumber)

        self.__teamsDrivers = teamsDrivers

        self.__qualificationResults = {result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]: result \
            for result in super(OneXTwo, self).getQualificationResults()}
        self.__raceResults = {result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]: result \
            for result in super(OneXTwo, self).getRaceResults()}

        self.__qualificationRow = self.__parseQualificationRow()
        self.__raceRow = self.__parseRaceRow()

    def __parseQualificationRow(self):
        return ""

    def __parseRaceRow(self):
        return ""

    def getQualificationRow(self):
        return self.__qualificationRow

    def getRaceRow(self):
        return self.__raceRow

    def getQualificationResults(self):
        return self.__raceResults
