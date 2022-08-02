import requests

url = "https://v3.football.api-sports.io/"

headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "7f3f43fa12159287758ccaa19595ed77"
        }

def getPlayerSquads(teamId):

    endpoint = "players/squads"
    querystring = {"team":teamId}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    player = response.json()


    return player['response']

def getLeagueStandings(leagueId, season):

    endpoint = "standings"
    querystring = {"league":leagueId,"season":season}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    players = response.json()

    return players['response']



def getPlayerStatsBySeason(playerId, season):

    endpoint = "players"
    querystring = {"id":playerId,"season":season}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    player = response.json()

    return player['response']


def getAllPlayerStatsInLeagueBySeason(leagueId, season, page):

    endpoint = "players"
    querystring = {"league":leagueId,"season":season, "page":page}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    players = response.json()

    return players['response']


def getAllPlayerStatsInTeamBySeason(teamId, season, page):

    endpoint = "players"
    querystring = {"team":teamId,"season":season, "page":page}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    players = response.json()

    return players['response']


