import requests


class ErgastQuerier(object):
    def __init__(self, series, season, roundNumber):
        self.__series = series
        self.__season = season
        self.__roundNumber = roundNumber

        self.__qualificationUrl = "http://ergast.com/api/" + self.__series + "/" + \
            self.__season + "/" + self.__roundNumber + "/qualifying.json"
        self.__raceUrl = "http://ergast.com/api/" + self.__series + "/" + \
            self.__season + "/" + self.__roundNumber + "/results.json"

        qualification = requests.get(self.__qualificationUrl).json()
        race = requests.get(self.__raceUrl).json()

        self.__roundName = race["MRData"]["RaceTable"]["Races"][0]["raceName"]
        self.__qualificationResults = qualification["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]
        self.__raceResults = race["MRData"]["RaceTable"]["Races"][0]["Results"]

    def getQualificationResults(self):
        return self.__qualificationResults

    def getRaceResults(self):
        return self.__raceResults

    def getRoundName(self):
        return self.__roundName
