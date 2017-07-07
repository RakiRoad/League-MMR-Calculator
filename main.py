import riot
import time
import tkinter as tk

LARGE_FONT=("Verdana", 12)


def main(name, displayResult):
    summonerName = " "
    realsummonerName = " "
    region = "NA1"

    tempName = str(name)
    print (tempName)

    if " " in tempName:
        summonerName = tempName.replace(" ", "%20")
        print (summonerName)
        realsummonerName = tempName
    elif " " not in tempName:
        summonerName = tempName
        realsummonerName = tempName

    time.sleep(10)
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

        time.sleep(2.5)

    #//////////////////////////////////////////////////////////////////////////////////////////////////////
    #The logic portion of the code
    #//////////////////////////////////////////////////////////////////////////////////////////////////////

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

    #This is calculates where the user mmr should actually be
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

    if realMMR > userTotal:
        outText = "You will skip a division! Your MMR, " + str(realMMR) + ", is higher than the average of " + str(userTotal)
        displayResult.set(outText)
    elif realMMR < userTotal:
        outText = "You are in Elo Hell Fam! Your MMR, " + str(realMMR) + ", is lower than the average of " + str(userTotal)
        displayResult.set(outText)
    else:
        displayResult.set("Your MMR is average")

#===============================================================================================

#===============================================================================================

class mmrCalc(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
    
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            
            label = tk.Label(self, text ="LOL MMR CALCULATOR", font = LARGE_FONT)
            label.pack(padx=100, pady=100)
            
            form1 = tk.Entry(self)
            form1.pack()

            v = tk.StringVar(self)

            button1 = tk.Button(self, text= "FIND MY MMR!", command=lambda: main(form1.get(), v))
            button1.pack()

            label2 = tk.Label(self, textvariable = v, font = LARGE_FONT)
            label2.pack()

#Initializes the Program
app = mmrCalc()
app.mainloop()