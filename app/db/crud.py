from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.playerID == player_id).first()

def get_player_stats(db: Session, player_id: int, season: int):
    results = db.query(models.Player, models.Playerstats).join(models.Playerstats).filter(models.Player.playerID == player_id, models.Playerstats.season == season).first()

    if results is None:
        return None
    return results[1]

def create_player(db: Session, player: schemas.Player):
    db_player = models.Player(playerID=player.playerID, name = player.name, firstName = player.firstName, lastName = player.lastName,
    age = player.age, birthDate = player.birthDate, birthPlace = player.birthPlace,
    birthCountry = player.birthCountry, nationality = player.nationality, height = player.height, weight = player.weight,
    injured = player.injured, photo = player.photo)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.teamID == team_id).first()

def create_team(db: Session, team: schemas.Team):
    db_team = models.Team(teamID = team.teamID, name = team.name, logo = team.logo)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_competition(db: Session, competition_id: int):
    return db.query(models.Competition).filter(models.Competition.competitionID == competition_id).first()

def get_competitionStandings(db: Session, competition_id: int, team_id : int, season : int):
    return db.query(models.Competitionstanding).filter(models.Competitionstanding.competitionID == competition_id, models.Competitionstanding.teamID == team_id, models.Competitionstanding.season == season).first()

def get_top_scorer(db: Session, season: int):
    results = db.query(func.max(models.Playerstats.goals)).filter(models.Playerstats.season == season).first()
    return results

def get_top_assister(db: Session, season: int):
    results = db.query(func.max(models.Playerstats.assists)).filter(models.Playerstats.season == season).first()
    return results

def get_top_fouls_drawn(db: Session, season: int):
    results = db.query(func.max(models.Playerstats.foulsDrawn)).filter(models.Playerstats.season == season).first()
    return results

def get_top_penalties_won(db: Session, season: int):
    results = db.query(func.max(models.Playerstats.penaltyWon)).filter(models.Playerstats.season == season).first()
    return results

def get_top_tackles_won(db: Session, season: int):
    results = db.query(func.max(models.Playerstats.tackles)).filter(models.Playerstats.season == season).first()
    return results

def get_top_interception_won(db: Session, season: int):
    results = db.query(func.max(models.Playerstats.interceptions)).filter(models.Playerstats.season == season).first()
    return results

def get_top_blocks(db: Session, season: int):
    results = db.query(func.max(models.Playerstats.blocks)).filter(models.Playerstats.season == season).first()
    return results

def get_top_fouls_committed(db: Session, season: int):
    results = db.query(func.max(models.Playerstats.foulsCommitted)).filter(models.Playerstats.season == season).first()
    return results

def get_team_competition_details(db: Session, team_id: int, season: int):
    results = db.query(models.Team, models.Competitionstanding, models.Competition).select_from(models.Team).join(models.Competitionstanding).join(models.Competition).filter(models.Team.teamID == team_id, models.Competitionstanding.season == season).all()
    return results

def get_similar_players_attacker(db: Session, season: int, playerID : int, position : str,
        totalShotsLowLimit: int, 
        totalShotsHighLimit : int,
        shotsOnTargetLowLimit : int,
        shotsOnTargetHighLimit : int,
        assistLowLimit : int,
        assistHighLimit : int,
        goalsLowLimit : int,
        goalsHighLimit : int,
        succesfulDribblesLowLimit : int,
        succesfulDribblesHighLimit : int):
    results = db.query(models.Player, models.Playerstats).join(models.Playerstats).filter(models.Playerstats.totalShots.between(totalShotsLowLimit, totalShotsHighLimit), models.Playerstats.shotsOnTarget.between(shotsOnTargetLowLimit, shotsOnTargetHighLimit),
    models.Playerstats.assists.between(assistLowLimit, assistHighLimit), models.Playerstats.goals.between(goalsLowLimit, goalsHighLimit), models.Playerstats.successfulDribbles.between(succesfulDribblesLowLimit, succesfulDribblesHighLimit), models.Player.playerID != playerID, models.Playerstats.season == season,
    models.Playerstats.position == position).all()
    return results

def get_similar_players_midfielder(db: Session, season: int, playerID : int, position : str,
        passAccuracyLowLimit: int, 
        passAccuracyHighLimit : int,
        shotsOnTargetLowLimit : int,
        shotsOnTargetHighLimit : int,
        assistLowLimit : int,
        assistHighLimit : int,
        goalsLowLimit : int,
        goalsHighLimit : int,
        succesfulDribblesLowLimit : int,
        succesfulDribblesHighLimit : int,
        totalPassesLowLimit : int, 
        totalPasesHighLimit : int):
    results = db.query(models.Player, models.Playerstats).join(models.Playerstats).filter(models.Playerstats.totalShots.between(passAccuracyLowLimit, passAccuracyHighLimit), models.Playerstats.shotsOnTarget.between(shotsOnTargetLowLimit, shotsOnTargetHighLimit),
    models.Playerstats.assists.between(assistLowLimit, assistHighLimit), models.Playerstats.goals.between(goalsLowLimit, goalsHighLimit), models.Playerstats.successfulDribbles.between(succesfulDribblesLowLimit, succesfulDribblesHighLimit), models.Player.playerID != playerID, models.Playerstats.season == season,
    models.Playerstats.position == position, models.Playerstats.totalPasses.between(totalPassesLowLimit, totalPasesHighLimit)).all()
    return results


def get_all_team_players(db: Session, team_id: int, season: int):
    results = db.query(models.Player, models.Playerstats, models.Team).select_from(models.Player).join(models.Playerstats).join(models.Team).filter(models.Team.teamID == team_id, models.Playerstats.season == season).all()

    #playerList = []
    #for x in results:
       # playerList.append(x[1])
    
    return results
