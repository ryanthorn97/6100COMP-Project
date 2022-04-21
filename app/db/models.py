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

    

    
    

    


#player = Table(
    #'player', meta,
    #Column('playerID', Integer, primary_key=True),
    #Column('name', String(45)),
    #Column('firstName', String(45)),
    #Column('lastName', String(45)),
    #Column('age', Integer),
    #Column('birthDate', Date),
    #Column('birthPlace', String(45)),
    #Column('birthCountry', String(45)),
    #Column('nationality', String(45)),
    #Column('height', String(45)),
    #Column('weight', String(45)),
    #Column('injured', Boolean),
    #Column('photo', String(45)),
#)

#team = Table(
    #'team', meta,
    #Column('teamID', Integer, primary_key=True),
    #Column('name', String(45)),
    #Column('logo', String(45)),
#)

#competition = Table(
    #'competition', meta,
    #Column('competitionID', Integer, primary_key=True),
    #Column('name', String(45)),
    #Column('country', String(45)),
    #Column('logo', String(45)),
    #Column('flag', String(45)),
    #Column('season', Integer),
#)

#competitionstanding = Table(
    #'competitionstanding', meta,
    #Column('competitionID', Integer, primary_key=True),
    #Column('name', String(45)),
    #Column('country', String(45)),
    #Column('logo', String(45)),
    #Column('flag', String(45)),
    #Column('season', Integer),
#)