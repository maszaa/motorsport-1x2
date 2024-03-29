import requests


class ErgastQuerierException(Exception):
    pass

class ErgastQuerier(object):
    def __init__(self, series, season, roundNumber):
        self.__series = series
        self.__season = season
        self.__roundNumber = roundNumber

        try:
            self.__qualifyingUrl = "http://ergast.com/api/" + self.__series + "/" + \
                str(self.__season) + "/" + str(self.__roundNumber) + "/qualifying.json"
            self.__raceUrl = "http://ergast.com/api/" + self.__series + "/" + \
                str(self.__season) + "/" + str(self.__roundNumber) + "/results.json"

            qualifying = requests.get(self.__qualifyingUrl)
            race = requests.get(self.__raceUrl)

            if qualifying.status_code != 200 or race.status_code != 200:
                raise ValueError("Invalid series, season or roundNumber!")

            self.__roundName = race.json()["MRData"]["RaceTable"]["Races"][0]["raceName"]
            self.__qualifyingResults = qualifying.json()["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]
            self.__raceResults = race.json()["MRData"]["RaceTable"]["Races"][0]["Results"]

        except (IndexError, ValueError):
            raise ErgastQuerierException("Invalid series, season or roundNumber!")
        except requests.ConnectionError:
            raise ErgastQuerierException("Problem with internet connection!")

    def getQualifyingResults(self):
        return self.__qualifyingResults

    def getRaceResults(self):
        return self.__raceResults

    def getRoundName(self):
        return self.__roundName
