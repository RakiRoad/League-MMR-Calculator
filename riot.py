import requests



def requestSummonersData(region, summonerName):
    #////////// Retrieves summoner Data \\\\\\\\\\

    #The api call url is created
    API = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName +"?api_key=" + myKey
    #Uses the "requests" package to retrieve the data in JSON format
    response = requests.get(API)
    #returns the JSON
    return response.json()

def requestsRankData(region, summonerID):
    #////////// Retrieves rank Data \\\\\\\\\\

    #The api call url is created 
    API = "https://" + region + ".api.riotgames.com/lol/league/v3/leagues/by-summoner/" + summonerID +"?api_key=" + myKey2
    #Uses the "requests" package to retrieve the data in JSON format
    response = requests.get(API)
    #returns the JSON
    return response.json()

def recentMatchData(region, accountID):
    #////////// Retrieves recent match data \\\\\\\\\\

    #The api call url is created 
    API = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + accountID +"/recent?api_key=" + myKey
    #Uses the "requests" package to retrieve the data in JSON format
    response = requests.get(API)
    #returns the JSON
    return response.json()

def summonersInGame(region, matchID):
    #////////// Retrieves list of summonersID's that player played with per game \\\\\\\\\\

    #The api call url is created 
    API = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + matchID +"?api_key=" + myKey
    #Uses the "requests" package to retrieve the data in JSON format
    response = requests.get(API)
    #returns the JSON
    return response.json()
