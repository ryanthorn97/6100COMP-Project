import requests

url = "https://v3.football.api-sports.io/"

headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "7f3f43fa12159287758ccaa19595ed77"
        }

async def getPlayerSquads(playerId):

    endpoint = "players/squads"
    querystring = {"player":playerId}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    player = response.json()

    return player['response']



async def getPlayerStatsBySeason(playerId, season):

    endpoint = "players"
    querystring = {"id":playerId,"season":season}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    player = response.json()

    return player['response']


async def getAllPlayerStatsInLeagueBySeason(leagueId, season, page):

    endpoint = "players"
    querystring = {"league":leagueId,"season":season, "page":page}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    players = response.json()

    return players['response']


async def getAllPlayerStatsInTeamBySeason(teamId, season, page):

    endpoint = "players"
    querystring = {"team":teamId,"season":season, "page":page}

    response = requests.request("GET", url + endpoint, headers=headers, params=querystring)

    players = response.json()

    return players['response']