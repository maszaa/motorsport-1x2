import requests


class ErgastQuerierException(Exception):
    pass

class ErgastQuerier(object):
    def __init__(self, series, season, roundNumber):
        self.__series = series
        self.__season = season
        self.__roundNumber = roundNumber

        try:
            self.__qualificationUrl = "http://ergast.com/api/" + self.__series + "/" + \
                self.__season + "/" + self.__roundNumber + "/qualifying.json"
            self.__raceUrl = "http://ergast.com/api/" + self.__series + "/" + \
                self.__season + "/" + self.__roundNumber + "/results.json"


            qualification = requests.get(self.__qualificationUrl)
            race = requests.get(self.__raceUrl)

            if qualification.status_code != 200 or race.status_code != 200:
                raise ValueError("Invalid series, season or roundNumber!")

            self.__roundName = race.json()["MRData"]["RaceTable"]["Races"][0]["raceName"]
            self.__qualificationResults = qualification.json()["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]
            self.__raceResults = race.json()["MRData"]["RaceTable"]["Races"][0]["Results"]

        except (IndexError, ValueError):
            raise ErgastQuerierException("Invalid series, season or roundNumber!")
        except requests.ConnectionError:
            raise ErgastQuerierException("Problem with internet connection!")

    def getQualificationResults(self):
        return self.__qualificationResults

    def getRaceResults(self):
        return self.__raceResults

    def getRoundName(self):
        return self.__roundName
