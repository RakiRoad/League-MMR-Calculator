import riot
import tkinter as tk
from tkinter import ttk

LARGE_FONT=("Comic Sans MS", 12)


def main(name, displayResult, rank, a, b ,c , d, e, f, g, h, rankText, regVal):
    summonerName = " "
    realsummonerName = " "


    tempName = str(name)
    tempRegion = str(regVal)

    if tempRegion == "NA":
        region = "NA1"
    elif tempRegion == "EUW":
        region = "EUW1"
    elif tempRegion == "EUNE":
        region = "EUN1"
    elif tempRegion == "KR":
        region = "KR"
    elif tempRegion == "JP":
        region = "JP1"
    elif tempRegion == "BR":
        region = "BR1"

    if " " in tempName:
        summonerName = tempName.replace(" ", "%20")
        realsummonerName = tempName
    elif " " not in tempName:
        summonerName = tempName
        realsummonerName = tempName

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
    responseJSON3 = riot.recentMatchData(region, accountID)
    game_ids = []
    for i in range (0, 4):
        game_ids.append(responseJSON3['matches'][i]['gameId'])
    
    #The API call
    game_1 = riot.summonersInGame(region, str(game_ids[0]))
    #game_2 = riot.summonersInGame(region, str(game_ids[1]))


    #where the player Id's of players are stored per game
    players_ids_1 = []
    players_ids_2 = []

    #where real summoner name are stored
    realName_1 = []
    realName_2 = []

    #Finds the player ID's for each game and put it in array
    for i in range (0, 10):
        players_ids_1.append(game_1['participantIdentities'][i]['player']['summonerId'])
        #players_ids_2.append(game_2['participantIdentities'][i]['player']['summonerId'])

        realName_1.append(game_1['participantIdentities'][i]['player']['summonerName'])
        #realName_2.append(game_2['participantIdentities'][i]['player']['summonerName'])

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
        rank.configure(image = b)
        rank.image = b
    elif rank_tier == "SILVER":
        userTier = 1000
        rank.configure(image = c)
        rank.image = c
    elif rank_tier == "GOLD":
        userTier = 2000
        rank.configure(image = d)
        rank.image = d
    elif rank_tier == "PLATINUM":
        userTier = 3000
        rank.configure(image = e)
        rank.image = e
    elif rank_tier == "DIAMOND":
        userTier = 4000
        rank.configure(image = f)
        rank.image = f
    elif rank_tier == "MASTER":
        userTier = 5000
        rank.configure(image = g)
        rank.image = g
    elif rank_tier == "CHALLENGER":
        userTier = 6000
        rank.configure(image = h)
        rank.image = h

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
        outText = "You will skip a division! Your MMR, " + str(realMMR) + ", is higher than your current division average of " + str(userTotal)
        displayResult.set(outText)
        rankText.set(str(rank_val))
    elif realMMR < userTotal:
        outText = "You are in Elo Hell Fam! Your MMR, " + str(realMMR) + ", is lower than your current division average of " + str(userTotal)
        displayResult.set(outText)
        rankText.set(str(rank_val))
    else:
        displayResult.set("Your MMR is average")
        rankText.set(str(rank_val))

#===============================================================================================

#===============================================================================================

class mmrCalc(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.title(self, "That Tasted Purple!")
        tk.Tk.iconbitmap(self, default="res/images/cupiconsmall.ico")

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

            photo = tk.PhotoImage(file="res/images/cupcakeSmall.png")
            pic1 = ttk.Label(self, image=photo)
            pic1.image = photo #keeps the reference
            pic1.grid(row = 0)

            label = ttk.Label(self, text ="THAT TASTED PURPLE!", font = LARGE_FONT)
            label.grid(row = 1, padx = 100, pady = 20)

            form1 = ttk.Entry(self, width=80)
            form1.grid(row = 2)

            v = tk.StringVar(self)
            rankText = tk.StringVar(self)
            regionSelect = tk.StringVar(self)
            
            regionSelect.set("NA")
            choices = ["NA", "EUW", "EUNE", "KR", "JP", "BR"]
            option  = ttk.OptionMenu(self, regionSelect, *choices)
            option.grid(row = 4, sticky="W", padx = 160)

            icon1 = tk.PhotoImage(file="res/rank/Blank2.png")
            icon2 = tk.PhotoImage(file="res/rank/Bronze.png")
            icon3 = tk.PhotoImage(file="res/rank/Silver.png")
            icon4 = tk.PhotoImage(file="res/rank/Gold.png")
            icon5 = tk.PhotoImage(file="res/rank/Platinum.png")
            icon6 = tk.PhotoImage(file="res/rank/Diamond.png")
            icon7 = tk.PhotoImage(file="res/rank/Master.png")
            icon8 = tk.PhotoImage(file="res/rank/Challenger.png")

            rank = ttk.Label(self, image=icon1)
            rank.image=icon1
            rank.grid(row=6)
            
            spacer = ttk.Label(self, text=" ")
            spacer.grid(row = 3)
            
            button1 = ttk.Button(self, text= "FIND MY MMR!", command=lambda: main(form1.get(), v, rank, icon1, icon2, icon3, icon4, icon5, icon6, icon7, icon8, rankText, regionSelect.get()))
            button1.grid(row = 4, columnspan=3, padx =150, sticky="E")
            form1.bind("<Return>", lambda event: main(form1.get(), v, rank, icon1, icon2, icon3, icon4, icon5, icon6, icon7, icon8, rankText, regionSelect.get()))

            label2 = ttk.Label(self, textvariable = v, font = LARGE_FONT)
            label2.grid(row = 5, padx = 100, pady = 25)

            label3 = ttk.Label(self, textvariable = rankText, font = LARGE_FONT)
            label3.grid(row = 7, padx = 100, pady= 20)

#Initializes the Program
app = mmrCalc()
app.mainloop()