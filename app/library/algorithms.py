from audioop import avg
from lib2to3.pgen2 import pgen
import math
from weakref import WeakSet

from sqlalchemy.orm import Session
from app.db import crud, schemas

from app.db.db import SessionLocal
from app.library import helpers

def teamWinChance(homeTeamQuality, AwayTeamQuality):

    homeAdvantage = 0.12
    randomnessIndicator = 0.23
    qualityDifference = homeTeamQuality - AwayTeamQuality

    score = 1 - math.exp(-((qualityDifference + homeAdvantage) / randomnessIndicator))
    return 0

def playerDefenceScore(db: Session, season: int, stats: schemas.Playerstats):
    topTackleList = []
    topInterceptionsList = []
    topBlocksList = []
    topFoulsCommittedList = []

    allStatsList = []

    #Calculate Tackles Perc
    for x in range(1,6):
        topTackleList.append(crud.get_top_tackles_won(db,(season-x)))
    
    topTackleList = [r[0] for r in topTackleList]

    tacklesPerc = helpers.calcStatPerc(stats.tackles, topTackleList)
    allStatsList.append(tacklesPerc)

    #Calculate Interceptions Perc
    for x in range(1,6):
        topInterceptionsList.append(crud.get_top_interception_won(db,(season-x)))
    
    topInterceptionsList = [r[0] for r in topInterceptionsList]

    interceptionsPerc = helpers.calcStatPerc(stats.interceptions, topInterceptionsList)
    allStatsList.append(interceptionsPerc)

    #Calculate Blocks Perc
    for x in range(1,6):
        topBlocksList.append(crud.get_top_blocks(db,(season-x)))
    
    topBlocksList = [r[0] for r in topBlocksList]

    blocksPerc = helpers.calcStatPerc(stats.blocks, topBlocksList)
    allStatsList.append(blocksPerc)

    #Calculate Fouls Committed Perc
    for x in range(1,6):
        topFoulsCommittedList.append(crud.get_top_fouls_committed(db,(season-x)))
    
    topFoulsCommittedList = [r[0] for r in topFoulsCommittedList]

    foulsPerc = helpers.calcStatPerc(stats.foulsCommitted, topFoulsCommittedList)
    allStatsList.append(foulsPerc)

    rating = stats.rating * 10
    passAccuracy = stats.passAccuracy
    duelsWonRatio = (stats.duelsWon/stats.duels) * 100
    
    allStatsList.extend((rating, passAccuracy, duelsWonRatio))

    print(allStatsList)

    weights = [0.15, 0.15, 0.1, 0.04, 0.4, 0.035, 0.125]

    for x in range(len(allStatsList)):
        allStatsList[x] = allStatsList[x] * weights[x] / sum(weights)
    finalDefenceScore = sum(allStatsList)

    print(finalDefenceScore)

    #print(goalsPerc, assistPerc, foulsDrawnPerc, penWonPerc)
    return round(finalDefenceScore, 1)


def playerAttackScore(db: Session, season: int, stats: schemas.Playerstats):
    
    topScoreList = []
    topAssistList = []
    topFoulsDrawnList = []
    topPenWonList = []

    allStatsList = []

    #Calculate Goals Perc
    for x in range(1,6):
        topScoreList.append(crud.get_top_scorer(db,(season-x)))
    
    topScoreList = [r[0] for r in topScoreList]

    goalsPerc = helpers.calcStatPerc(stats.goals, topScoreList)
    allStatsList.append(goalsPerc)

    #Calculate Assists Perc
    for x in range(1,6):
        topAssistList.append(crud.get_top_assister(db,(season-x)))
    
    topAssistList = [r[0] for r in topAssistList]

    assistPerc = helpers.calcStatPerc(stats.assists, topAssistList)
    allStatsList.append(assistPerc)
    
    #Calculate Fouls Drawn Perc
    for x in range(1,6):
        topFoulsDrawnList.append(crud.get_top_fouls_drawn(db,(season-x)))
    
    topFoulsDrawnList = [r[0] for r in topFoulsDrawnList]

    foulsDrawnPerc = helpers.calcStatPerc(stats.foulsDrawn, topFoulsDrawnList)
    allStatsList.append(foulsDrawnPerc)

    #Calculate Pen Won Perc
    for x in range(1,6):
        topPenWonList.append(crud.get_top_penalties_won(db,(season-x)))
    
    topPenWonList = [r[0] for r in topPenWonList]
    penWonPerc = helpers.calcStatPerc(stats.penaltyWon, topPenWonList)
    allStatsList.append(penWonPerc)

    rating = stats.rating * 10
    shotsOnTargetRatio = (stats.shotsOnTarget/stats.totalShots) * 100
    passAccuracy = stats.passAccuracy
    dribbleSuccessRatio = (stats.successfulDribbles/stats.dribbleAttempts) * 100

    allStatsList.extend((rating, shotsOnTargetRatio, passAccuracy, dribbleSuccessRatio))

    #print(allStatsList)

    weights = [0.2, 0.12, 0.07, 0.01, 0.33, 0.12, 0.08, 0.07]

    for x in range(len(allStatsList)):
        allStatsList[x] = allStatsList[x] * weights[x] / sum(weights)
    finalAttackScore = sum(allStatsList)

    #print(finalAttackScore)

    #print(goalsPerc, assistPerc, foulsDrawnPerc, penWonPerc)
    return round(finalAttackScore, 1)

def playerGKScore():
    return 0

def teamScore(db: Session, season: int, playerList : list):
    playerStatsList = []
    attackScores = []
    midfieldScores = []
    defenceScores = []
    gkScores = []
    avgScores = {"Forwards" : 0, "Midfielders" : 0, "Defenders" : 0, "Goalkeepers" : 0}
    
    for players in playerList:
        playerStatsList.append(players[1])
        print(players[0].name)
    
    for playerStats in playerStatsList:
        if playerStats.position == "Attacker":
            attackScores.append(playerAttackScore(db, season, playerStats))
        if playerStats.position == "Midfielder":
            midfieldScores.append(playerAttackScore(db, season, playerStats))
        if playerStats.position == "Defender":
            defenceScores.append(playerDefenceScore(db, season, playerStats))
        if playerStats.position == "Goalkeeper":
            defenceScores.append(playerDefenceScore(db, season, playerStats))

    if len(attackScores) != 0:
        avgAttackScore = sum(attackScores) / len(attackScores)
    else:
        avgAttackScore = 0
    avgScores["Forwards"] = avgAttackScore

    if len(midfieldScores) != 0:
        avgMidfieldScores = sum(midfieldScores) / len(midfieldScores)
    else:
        avgMidfieldScores = 0
    avgScores["Midfielders"] = avgMidfieldScores

    if len(defenceScores) != 0:
        avgDefenceScores = sum(defenceScores) / len(defenceScores)
    else:
        avgDefenceScores = 0
    avgScores["Defenders"] = avgDefenceScores
    
    if len(gkScores) != 0:
        avgGKScores = sum(gkScores) / len(gkScores)
    else:
        avgGKScores = 0
    avgScores["Goalkeepers"] = avgGKScores

    #avgScores.extend((avgAttackScore, avgMidfieldScores, avgDefenceScores, avgGKScores))
    weakestArea = min(avgScores, key=avgScores.get)

    if (len(attackScores) + len(midfieldScores) + len(defenceScores) + len(gkScores) != 0):
        teamScore = (sum(attackScores) + sum(midfieldScores) + sum(defenceScores) + sum(gkScores)) / (len(attackScores) + len(midfieldScores) + len(defenceScores) + len(gkScores))
        teamScore = round(teamScore, 1)
    else:
        teamScore = 0

    scoreDetails = {"teamScore" : teamScore, "weakestArea" : weakestArea} 

    #print(playerStatsList)
    print(avgScores["Forwards"], avgScores["Midfielders"], avgScores["Defenders"], avgScores["Goalkeepers"])
    print(teamScore)
    print(weakestArea)
    return scoreDetails

def comparePlayerStats(db: Session, season : int, player1Stats: schemas.Playerstats, player2Stats: schemas.Playerstats):

    if player1Stats.position == "Attacker":   
        player1Score = playerAttackScore(db, season, player1Stats)
    elif player1Stats.position == "Midfielder":
        player1Score = playerAttackScore(db, season, player1Stats)
    elif player1Stats.position == "Defender":
        player1Score = playerDefenceScore(db, season, player1Stats)
    elif player1Stats.position == "Goalkeeper":
        player1Score = playerGKScore(db, season, player1Stats)

    if player2Stats.position == "Attacker":   
        player2Score = playerAttackScore(db, season, player2Stats)
    elif player2Stats.position == "Midfielder":
        player2Score = playerAttackScore(db, season, player2Stats)
    elif player2Stats.position == "Defender":
        player2Score = playerDefenceScore(db, season, player2Stats)
    elif player2Stats.position == "Goalkeeper":
        player2Score = playerGKScore(db, season, player2Stats)

    similarity = round(helpers.num_sim(player1Score, player2Score), 2) *100
    print(similarity)

    scores = {"player1Score" : player1Score, "player2Score" : player2Score, "similarity" : similarity}

    return scores

def compareTeamStats():
    return 0

def estimatePlayerValue():
    return 0

def findSimilarPlayers(db: Session, season: int, stats: schemas.Playerstats):
    if stats.position == "Attacker":
        totalShotsLowLimit = round(stats.totalShots * 0.8)
        totalShotsHighLimit = round(stats.totalShots * 1.2)
        shotsOnTargetLowLimit = round(stats.shotsOnTarget * 0.8)
        shotsOnTargetHighLimit = round(stats.shotsOnTarget * 1.2)
        assistLowLimit = round(stats.assists * 0.8)
        assistHighLimit = round(stats.assists * 1.2)
        goalsLowLimit = round(stats.goals * 0.8)
        goalsHighLimit = round(stats.goals * 1.2)
        succesfulDribblesLowLimit = round(stats.successfulDribbles * 0.8)
        succesfulDribblesHighLimit = round(stats.successfulDribbles * 1.2)

        similarPlayers = crud.get_similar_players_attacker(db, season, stats.playerID, stats.position, totalShotsLowLimit, totalShotsHighLimit, shotsOnTargetLowLimit, shotsOnTargetHighLimit, assistLowLimit, assistHighLimit, goalsLowLimit, goalsHighLimit, succesfulDribblesLowLimit, succesfulDribblesHighLimit)
 
        if len(similarPlayers) == 0:
            return "no similar players available"


        for player, playerStats in similarPlayers:
            print(player.name, playerStats.position)
        #print(similarPlayers[0][0].name)
        return similarPlayers
        #score = playerAttackScore()

    elif stats.position == "Midfielder":
        passAccuracyLowLimit = round(stats.passAccuracy * 0.8)
        passAcuracyHighLimit = round(stats.passAccuracy * 1.2)
        shotsOnTargetLowLimit = round(stats.shotsOnTarget * 0.8)
        shotsOnTargetHighLimit = round(stats.shotsOnTarget * 1.2)
        assistLowLimit = round(stats.assists * 0.8)
        assistHighLimit = round(stats.assists * 1.2)
        goalsLowLimit = round(stats.goals * 0.8)
        goalsHighLimit = round(stats.goals * 1.2)
        succesfulDribblesLowLimit = round(stats.successfulDribbles * 0.8)
        succesfulDribblesHighLimit = round(stats.successfulDribbles * 1.2)
        totalPassesLowLimit = round(stats.totalPasses * 0.8)
        totalPassesHighLimit = round(stats.totalPasses * 1.2)

        similarPlayers = crud.get_similar_players_midfielder(db, season, stats.playerID, stats.position, passAccuracyLowLimit, passAcuracyHighLimit, shotsOnTargetLowLimit, shotsOnTargetHighLimit, assistLowLimit, assistHighLimit, goalsLowLimit, goalsHighLimit, succesfulDribblesLowLimit, succesfulDribblesHighLimit, totalPassesLowLimit, totalPassesHighLimit)
 
        if len(similarPlayers) == 0:
            return "no similar players available"


        for player, playerStats in similarPlayers:
            print(player.name, playerStats.position)
        #print(similarPlayers[0][0].name)
        return similarPlayers



