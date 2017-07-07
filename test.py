import riot
import time

def main():
    '''
    #TEST VALUES
    region = "NA1"
    #summonerName = "Raki%20Road"
    #realsummonerName = "Raki Road"
    summonerName = "ShadyCloud"
    realsummonerName = "ShadyCloud"
    #ID = "48536262"
    #accountID = "211741090"
    gameID = "2537568859"
    '''
    region = "NA1"
    summonerName = "ShadyCloud"
    realsummonerName = "ShadyCloud"

    #call used to find summonerID
    responseJSON  = riot.requestSummonersData(region, summonerName)
    ID = responseJSON['id']
    ID = str(ID)
    accountID = responseJSON['accountId']
    accountID = str(accountID)

    #call used to find ranked data prints the rank and division
    responseJSON2 = riot.requestsRankData(region, ID)
    arrayLength = len(responseJSON2[0]['entries'])

    #declaring rank global variables
    rank_tier = " "
    rank_division = " "
    rank_val = " "

    #sets the values to rank stuff
    for i in range (0, arrayLength):
        if responseJSON2[0]['entries'][i]['playerOrTeamName'] == realsummonerName:
            rank_tier = str(responseJSON2[0]['tier'])
            rank_division = str(responseJSON2[0]['entries'][i]['rank'])
            rank_val = str((responseJSON2[0]['tier'] + " " + responseJSON2[0]['entries'][i]['rank']))

    #Find the gameID's of summoner's 5 recent matches
    time.sleep(1)
    responseJSON3 = riot.recentMatchData(region, accountID)
    game_ids = []
    for i in range (0, 4):
        game_ids.append(responseJSON3['matches'][i]['gameId'])
    
    #The API call
    game_1 = riot.summonersInGame(region, str(game_ids[0]))
    game_2 = riot.summonersInGame(region, str(game_ids[1]))


    #where the player Id's of players are stored per game
    players_ids_1 = []
    players_ids_2 = []

    #where real summoner name are stored
    realName_1 = []
    realName_2 = []

    #Finds the player ID's for each game and put it in array
    for i in range (0, 10):
        players_ids_1.append(game_1['participantIdentities'][i]['player']['summonerId'])
        players_ids_2.append(game_2['participantIdentities'][i]['player']['summonerId'])

        realName_1.append(game_1['participantIdentities'][i]['player']['summonerName'])
        realName_2.append(game_2['participantIdentities'][i]['player']['summonerName'])

        #For accountIDs
        #players_ids.append(responseJSON4['participantIdentities'][i]['player']['accountId'])
    
    #print (players_ids_1)
    #print (realName_1)
    #print(" ")
    #print (players_ids_2)
    #print (realName_2)
    
    #game list 1
    rank_tier_1 = []
    rank_division_1 = []
    rank_val_1 = []

    #game list 2
    rank_tier_2 = []
    rank_division_2 = []
    rank_val_2 = []

    for j in range (0, 10):
        testJSON = riot.requestsRankData(region, str(players_ids_1[j]))
        arrayLength = len(testJSON[0]['entries'])


        #sets the values to rank stuff
        for i in range (0, arrayLength):
            if testJSON[0]['entries'][i]['playerOrTeamName'] == realName_1[j]:
                rank_tier_1.append(str(testJSON[0]['tier']))
                rank_division_1.append(str(testJSON[0]['entries'][i]['rank']))
                rank_val_1.append(str((testJSON[0]['tier'] + " " + testJSON[0]['entries'][i]['rank'])))

        #print (rank_val_1[j])
        time.sleep(2.5)
    #print (" ")


    #where assigned weights will be stored
    totalTier = []
    totalDivision = []

    #Assign weights to other summoner's Division
    for i in range (0, 10):

        if rank_tier_1[i] == "BRONZE":
            totalTier.append(0)
        elif rank_tier_1[i] == "SILVER":
            totalTier.append(1000)
        elif rank_tier_1[i] == "GOLD":
            totalTier.append(2000)
        elif rank_tier_1[i] == "PLATINUM":
            totalTier.append(3000)
        elif rank_tier_1[i] == "DIAMOND":
            totalTier.append(4000)
        elif rank_tier_1[i] == "MASTER":
            totalTier.append(5000)
        elif rank_tier_1[i] == "CHALLENGER":
            totalTier.append(6000)
    for i in range (0, 10):

        if rank_division_1[i] == "V":
            totalDivision.append(0)
        elif rank_division_1[i] == "IV":
            totalDivision.append(200)
        elif rank_division_1[i] == "III":
            totalDivision.append(400)
        elif rank_division_1[i] == "II":
            totalDivision.append(600)
        elif rank_division_1[i] == "I":
            totalDivision.append(800)
    
    
    MMRcompare = (sum(totalTier) / float(len(totalDivision))) + (sum(totalDivision) / float(len(totalDivision)))

    userTier = 0
    userDivision = 0

    if rank_tier == "BRONZE":
        userTier = 0
    elif rank_tier == "SILVER":
        userTier = 1000
    elif rank_tier == "GOLD":
        userTier = 2000
    elif rank_tier == "PLATINUM":
        userTier = 3000
    elif rank_tier == "DIAMOND":
        userTier = 4000
    elif rank_tier == "MASTER":
        userTier = 5000
    elif rank_tier == "CHALLENGER":
        userTier = 6000

    if rank_division == "V":
        userDivision = 0
    elif rank_division == "IV":
        userDivision = 200
    elif rank_division == "III":
        userDivision = 400
    elif rank_division == "II":
        userDivision = 600
    elif rank_division == "I":
        userDivision = 800
    
    userTotal = userTier + userDivision

    realMMR = (userTotal + MMRcompare) / 2

    #print (totalTier)
    #print (totalDivision)
    #print (MMRcompare)
    #print (" ")
    #print(userTotal)
    
    if realMMR > userTotal:
        print("Your MMR, " + str(realMMR) + ", is higher than the average of " + str(userTotal))
    elif realMMR < userTotal:
        print("Your MMR, " + str(realMMR) + ", is lower than the average of " + str(userTotal))
    else:
        print("Your MMR is average")


if __name__ == "__main__":
    main()