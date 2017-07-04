import requests

#API key = 6c14dd62-6922-4419-8969-d149c8ab39c4
#Raki Road summonerID = 48536262

def requestSummonersData(region, summonerName):
    #////////// Retrieves summoner Data \\\\\\\\\\

    #The api call url is created
    API = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName +"?api_key=6c14dd62-6922-4419-8969-d149c8ab39c4"
    #Uses the "requests" package to retrieve the data in JSON format
    response = requests.get(API)
    #returns the JSON
    return response.json()

def requestsRankData(region, summonerID):
    #////////// Retrieves rank Data \\\\\\\\\\

    #The api call url is created 
    API = "https://" + region + ".api.riotgames.com/lol/league/v3/leagues/by-summoner/" + summonerID +"?api_key=6c14dd62-6922-4419-8969-d149c8ab39c4"
    #Uses the "requests" package to retrieve the data in JSON format
    response = requests.get(API)
    #returns the JSON
    return response.json()

def recentMatchData(region, accountID):
    #////////// Retrieves recent match data \\\\\\\\\\

    #The api call url is created 
    API = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + accountID +"/recent?api_key=6c14dd62-6922-4419-8969-d149c8ab39c4"
    #Uses the "requests" package to retrieve the data in JSON format
    response = requests.get(API)
    #returns the JSON
    return response.json()

def summonersInGame(region, matchID):
    #////////// Retrieves list of summonersID's that player played with per game \\\\\\\\\\

    #The api call url is created 
    API = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + matchID +"?api_key=6c14dd62-6922-4419-8969-d149c8ab39c4"
    #Uses the "requests" package to retrieve the data in JSON format
    response = requests.get(API)
    #returns the JSON
    return response.json()

#
#
#
#
#

def main():

    #Need to implement functionality that asks user for username and region
    #Need to implement functionality that replaces spaces with "%20"

    #TEST VALUES
    region = "NA1"
    #summonerName = "Raki%20Road"
    #realsummonerName = "Raki Road"
    summonerName = "ShadyCloud"
    realsummonerName = "ShadyCloud"
    #ID = "48536262"
    #accountID = "211741090"
    gameID = "2537568859"

    #call used to find summonerID
    responseJSON  = requestSummonersData(region, summonerName)
    ID = responseJSON['id']
    ID = str(ID)
    accountID = responseJSON['accountId']
    accountID = str(accountID)

    #call used to find ranked data prints the rank and division
    responseJSON2 = requestsRankData(region, ID)
    arrayLength = len(responseJSON2[0]['entries'])
    for i in range (0, arrayLength):
        if responseJSON2[0]['entries'][i]['playerOrTeamName'] == realsummonerName:
            print (responseJSON2[0]['tier'] + " " + responseJSON2[0]['entries'][i]['rank'])

    #Find the gameID's of summoner's 5 recent matches
    responseJSON3 = recentMatchData(region, accountID)
    game_ids = []
    for i in range (0, 5):
        game_ids.append(responseJSON3['matches'][i]['gameId'])
    
    #Finds the summoner ID's of recently played summoners per game
    responseJSON4 = summonersInGame(region, str(game_ids[0]))
    players_ids = []
    for i in range (0, 9):
        players_ids.append(responseJSON4['participantIdentities'][i]['player']['summonerId'])
        #For accountIDs
        #players_ids.append(responseJSON4['participantIdentities'][i]['player']['accountId'])
    print(players_ids)

#Starts the program
if __name__ == "__main__":
    main()