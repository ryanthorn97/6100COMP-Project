from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Player(Base):
    __tablename__ = "player"

    playerID = Column(Integer, primary_key=True)
    name = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    age = Column(Integer)
    birthDate = Column(Date)
    birthPlace = Column(String)
    birthCountry = Column(String)
    nationality = Column(String)
    height = Column(String)
    weight = Column(String)
    injured = Column(Boolean)
    photo = Column(String, nullable=True)

    playerstats = relationship("Playerstats", back_populates="player")

class Team(Base):
    __tablename__ = "team"

    teamID = Column(Integer, primary_key=True)
    name = Column(String)
    logo = Column(String, nullable=True)

    competitions = relationship("Competitionstanding", back_populates="team")
    teamstats = relationship("Teamstats", back_populates="team")

class Competition(Base):
    __tablename__ = "competition"

    competitionID = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    logo = Column(String, nullable=True)
    flag = Column(String, nullable=True)

    teams = relationship("Competitionstanding", back_populates="competition")

    
class Competitionstanding(Base):
    __tablename__ = "competitionstanding"

    competitionID = Column(
        Integer, 
        ForeignKey('competition.competitionID'), 
        primary_key=True)
    teamID = Column(
        Integer, 
        ForeignKey('team.teamID'), 
        primary_key=True)
    season = Column(Integer, primary_key=True)
    rank = Column(Integer)
    points = Column(Integer)
    form = Column(String)
    description = Column(String)

    team = relationship("Team", back_populates="competitions")
    competition = relationship("Competition", back_populates="teams")

class Playerstats(Base):
    __tablename__ = "playerstats"

    playerStatsID = Column(Integer, primary_key=True)
    playerID = Column(Integer, ForeignKey('player.playerID'))
    teamID = Column(Integer, ForeignKey('team.teamID'))
    competitionID = Column(Integer, ForeignKey('competition.competitionID'))
    season = Column(Integer)
    appearances = Column(Integer)
    lineups = Column(Integer)
    minutes = Column(Integer)
    number = Column(Integer, nullable=True)
    position = Column(String)
    rating = Column(Float)
    captain = Column(Boolean)
    totalShots = Column(Integer)
    shotsOnTarget = Column(Integer)
    goals = Column(Integer)
    goalsConceded = Column(Integer)
    assists = Column(Integer)
    saves = Column(Integer)
    totalPasses = Column(Integer)
    keyPasses = Column(Integer)
    passAccuracy = Column(Integer)
    tackles = Column(Integer)
    blocks = Column(Integer)
    interceptions = Column(Integer)
    duels = Column(Integer)
    duelsWon = Column(Integer)
    dribbleAttempts = Column(Integer)
    successfulDribbles = Column(Integer)
    foulsDrawn = Column(Integer)
    foulsCommitted = Column(Integer)
    yellowCards = Column(Integer)
    doubleYellowCards = Column(Integer)
    redCards = Column(Integer)
    penaltyWon = Column(Integer)
    penaltyCommitted = Column(Integer)
    penaltyScored = Column(Integer)
    penaltyMissed = Column(Integer)
    penaltySaved = Column(Integer)

    player = relationship("Player", foreign_keys=[playerID])
    team = relationship("Team", foreign_keys=[teamID])
    competition = relationship("Competition", foreign_keys=[competitionID])

class Teamstats(Base):
    __tablename__ = "teamstats"

    teamStatsID = Column(Integer, primary_key=True)
    teamID = Column(Integer, ForeignKey('team.teamID'))
    competitionID = Column(Integer, ForeignKey('competition.competitionID'))
    season = Column(Integer)
    avgGoalsAgAway = Column(Integer)
    avgGoalsAgHome = Column(Integer)
    avgGoalsAgTotal = Column(Integer)
    avgGoalsForAway = Column(Integer)
    avgGoalsForHome = Column(Integer)
    avgGoalsForTotal = Column(String)
    biggestGoalsForHome = Column(Integer)
    biggestGoalsForAway = Column(Integer)
    biggestGoalsAgHome = Column(Integer)
    biggestGoalsAgAway = Column(Integer)
    biggestLossAway = Column(String)
    biggestLossHome = Column(String)
    biggestDrawStreak = Column(Integer)
    biggestWinStreak = Column(Integer)
    biggestLoseStreak = Column(Integer)
    biggestWinAway = Column(String)
    biggestWinHome = Column(String)
    yellowCards = Column(Integer)
    redCards = Column(Integer)
    homeCleanSheet = Column(Integer)
    awayCleanSheet = Column(Integer)
    totalCleanSheet = Column(Integer)
    failedToScoreAway = Column(Integer)
    failedToScoreHome = Column(Integer)
    totalFailedToScore = Column(Integer)
    drawsHome = Column(Integer)
    drawsAway = Column(Integer)
    drawsTotal = Column(Integer)
    lossHome = Column(Integer)
    lossAway = Column(Integer)
    lossTotal = Column(Integer)
    playedHome = Column(Integer)
    playedAway = Column(Integer)
    playedTotal = Column(Integer)
    winsAway = Column(Integer)
    winsHome = Column(Integer)
    winsTotal = Column(Integer)
    penaltyMissedPerc = Column(String)
    penaltyMissedTotal = Column(Integer)
    penaltyScoredPerc = Column(String)
    penaltyScoredTotal = Column(Integer)    

    team = relationship("Team", back_populates="teamstats")
