from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.db import SessionLocal
from sqlalchemy.orm import Session

from app.db import schemas, crud, models
from app.library import algorithms
from app.library.helpers import common_data

from app.services.apifootball import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")

@router.get("/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@router.get("/players/stats/{player_id}", response_model=schemas.Playerstats)
def read_player_stats(player_id: int, db: Session = Depends(get_db), season : Optional[int] = 2021):
    db_player = crud.get_player_stats(db, player_id=player_id, season=season)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player stats not found for season " + str(season))
    return db_player

@router.get("/players/team/{player_id}", response_model=schemas.Team)
def read_player_team(player_id: int, db: Session = Depends(get_db), season : Optional[int] = 2021):
    db_player = crud.get_players_team(db, player_id, season)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player team not found for season " + str(season))
    return db_player

@router.post("/players/", response_model=schemas.Player)
def create_player(player: schemas.Player, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player.playerID)
    if db_player is not None:
        raise HTTPException(status_code=400, detail="Player already exists in db")
    else:
        return crud.create_player(db=db, player=player)


@router.get("/apiplayers/{player_id}")
def get_api_player(player_id: int, season : Optional[int] = 2021):
    stats = getPlayerStatsBySeason(player_id, season)
    if len(stats)==0:
        return False
    return stats[0]

@router.get("/apiplayers/squads/{team_id}")
def get_api_player_squads(team_id: int):
    squads = getPlayerSquads(team_id)
    #data = squads[0]
    #return squads
    if len(squads)==0:
        return False
    return squads[0]

def addAllPlayersDB():
    db = SessionLocal()

    teamIDs = db.query(models.Team.teamID).all()
    teamIDs = [r[0] for r in teamIDs]

    playerIDs = []
 
    for x in teamIDs:
        squadData = get_api_player_squads(x)

        if squadData != False:

            squadData = squadData["players"]
            for IDs in squadData:
                playerIDs.append(IDs["id"])

    for x in playerIDs:
        data = get_api_player(x)

        if data != False:

            data = data["player"]

            db_player = crud.get_player(db, x)

            if db_player is not None:
                    pass
            else:
                p = models.Player()
                p.playerID = x
                p.name = data["name"]
                p.firstName = data["firstname"]
                p.lastName = data["lastname"]
                p.age = data["age"]
                p.birthDate = data["birth"]["date"]
                p.birthPlace = data["birth"]["place"]
                p.birthCountry = data["birth"]["country"]
                p.nationality = data["nationality"]
                p.height = data["height"]
                p.weight = data["weight"]
                p.injured = data["injured"]
                p.photo = data["photo"]
                
                db.add(p)
                db.commit()
                print(p.name + " added to db")
                    
            db.close()



@router.get("/players/league/{league_id}")
def get_players_stats_by_league(league_id: int, season: int, page: int):
    data = getAllPlayerStatsInLeagueBySeason(league_id, season, page)
    return data

@router.get("/players/team/{team_id}")
def get_players_stats_by_team(team_id: int, season: int, page: int):
    data = getAllPlayerStatsInTeamBySeason(team_id, season, page)
    return data


@router.get("/playerpage/", response_class=HTMLResponse)
def player_page(request: Request, player_id: int, season : Optional[int] = 2021, db: Session = Depends(get_db)):
    data =  read_player(player_id, db)
    stats = read_player_stats(player_id, db, season)
    team = read_player_team(player_id, db, season)
    if stats.position == "Attacker":   
        score = algorithms.playerAttackScore(db, season, stats)
    elif stats.position == "Midfielder":
        score = algorithms.playerAttackScore(db, season, stats)
    elif stats.position == "Defender":
        score = algorithms.playerDefenceScore(db, season, stats)
    elif stats.position == "Goalkeeper":
        score = algorithms.playerGKScore(db, season, stats)
    
    value = algorithms.estimatePlayerValue(db, season, data, stats, score)

    return templates.TemplateResponse("player.html", {"request": request, "data": data, 'stats': stats, 'team': team, 'score': score, "value" : value})

@router.get("/searchplayers")
def search_players(request: Request, query: Optional[str], db: Session = Depends(get_db)):
    players = db.query(models.Player).filter(models.Player.name.contains(query)).all()
    #return players
    return templates.TemplateResponse(
        "search.html", {"request": request, "players": players}
    )

@router.get("/compareplayers")
def compare_players(request: Request, query: int, player_id: int, db: Session = Depends(get_db)):
    player1 = read_player(player_id, db)
    player2 = read_player(query, db)
    player1Stats = read_player_stats(player_id, db)
    player2Stats = read_player_stats(query, db)

    scores = algorithms.comparePlayerStats(db, 2021, player1Stats, player2Stats)

    player1Score = scores["player1Score"]
    player2Score = scores["player2Score"]
    similarity = scores["similarity"]

    if player2 is None or player1 is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return templates.TemplateResponse(
        "playercompare.html", {"request": request, "player1": player1, "player1Stats": player1Stats,
         "player1Score": player1Score, "player2": player2, "player2Stats": player2Stats,
          "player2Score": player2Score, "similarity": similarity}
    )

@router.get("/similarplayers/{player_id}")
def similar_players(request: Request, player_id: int, season : Optional[int] = 2021, db: Session = Depends(get_db)):
    stats = read_player_stats(player_id, db)
    similarPlayers = algorithms.findSimilarPlayers(db, season, stats)

    return templates.TemplateResponse(
        "search.html", {"request": request, "similarPlayers": similarPlayers}
    )
