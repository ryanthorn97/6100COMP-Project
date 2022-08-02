from datetime import date

from pydantic import BaseModel

class Player(BaseModel):
    playerID : int
    name : str
    firstName : str
    lastName : str
    age : int
    birthDate : date
    birthPlace : str
    birthCountry : str
    nationality : str
    height : str
    weight : str
    injured : bool
    photo : str

    class Config:
        orm_mode = True

class Team(BaseModel):
    teamID : int
    name : str
    logo : str

    class Config:
        orm_mode = True

class Competition(BaseModel):
    competitionID : int
    name : str
    country : str
    logo : str
    flag : str

    class Config:
        orm_mode = True

class Competitionstanding(BaseModel):
    competitionID : int
    teamID : int
    season : int
    rank : int
    points : int
    form : str
    description : str

    class Config:
        orm_mode = True

class Playerstats(BaseModel):
    playerStatsID : int
    playerID : int
    teamID : int
    competitionID : int
    season : int
    appearances : int
    lineups : int
    minutes : int
    number : int
    position : str
    rating : float
    captain  : bool
    totalShots : int
    shotsOnTarget : int
    goals : int
    goalsConceded : int
    assists : int
    saves : int
    totalPasses : int
    keyPasses : int
    passAccuracy : int
    tackles : int
    blocks : int
    interceptions : int
    duels : int
    duelsWon : int
    dribbleAttempts : int
    successfulDribbles : int
    foulsDrawn : int
    foulsCommitted : int
    yellowCards : int
    doubleYellowCards : int
    redCards : int
    penaltyWon : int
    penaltyCommitted : int
    penaltyScored : int
    penaltyMissed : int
    penaltySaved : int

    class Config:
        orm_mode = True
    
class Teamstats(BaseModel):
    teamStatsID : int
    teamID : int
    competitionID : int
    season : int
    avgGoalsAgAway : int
    avgGoalsAgHome : int
    avgGoalsAgTotal : int
    avgGoalsForAway : int
    avgGoalsForHome : int
    avgGoalsForTotal : int
    biggestGoalsForHome : int
    biggestGoalsForAway : int
    biggestGoalsAgHome : int
    biggestGoalsAgAway : int
    biggestLossAway : str
    biggestLossHome : str
    biggestDrawStreak : int
    biggestWinStreak : int
    biggestLoseStreak : int
    biggestWinAway : str
    biggestWinHome : str
    yellowCards : int
    redCards : int
    homeCleanSheet : int
    awayCleanSheet : int
    totalCleanSheet : int
    failedToScoreAway : int
    failedToScoreHome : int
    totalFailedToScore : int
    drawsHome : int
    drawsAway : int
    drawsTotal : int
    lossHome : int
    lossAway : int
    lossTotal : int
    playedHome : int
    playedAway : int
    playedTotal : int
    winsAway : int
    winsHome : int
    winsTotal : int
    penaltyMissedPerc : str
    penaltyMissedTotal : int
    penaltyScoredPerc : str
    penaltyScoredTotal : int 

    class Config:
        orm_mode = True