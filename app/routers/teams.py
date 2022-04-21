from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import null
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.db import SessionLocal
from sqlalchemy.orm import Session

from app.db import schemas, crud, models
from app.library.algorithms import teamScore

from app.services.apifootball import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")


@router.get("/teams/{team_id}", response_model=schemas.Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.get("/teamcompetition/{team_id}")
def read_team_competition(team_id: int, db: Session = Depends(get_db), season : Optional[int] = 2021):
    db_team = crud.get_team_competition_details(db, team_id=team_id, season=season)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.get("/teamplayers/{team_id}")
def read_team_players(team_id: int, db: Session = Depends(get_db), season : Optional[int] = 2021):
    db_team = crud.get_all_team_players(db, team_id=team_id, season=season)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.Team, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team.teamID)
    if db_team is not None:
        raise HTTPException(status_code=400, detail="Team already exists in db")
    else:
        return crud.create_team(db=db, team=team)

@router.get("/apicompetitions/{competition_id}")
def get_api_competition(competition_id: int, season : Optional[int] = 2021):
    stats = getLeagueStandings(competition_id, season)

    data = stats[0]["league"]["standings"][0]

    return data

@router.get("/searchteams")
def search_teams(request: Request, query: Optional[str], db: Session = Depends(get_db)):
    teams = db.query(models.Team).filter(models.Team.name.contains(query)).all()
    return teams

def addAllTeams(leagueID, year):
    db = SessionLocal()

    data = get_api_competition(leagueID, year)

    for team in data:
        t = models.Team()
        t.teamID = team["team"]["id"]
        t.name = team["team"]["name"]
        t.logo = team["team"]["logo"]

        db_team = crud.get_team(db, t.teamID)
        if db_team is not None or t.name == "Arles-Avignon":
            pass
        else:
            db.add(t)
            db.commit()
            print(t.name + " added to db")
        
        db.close()
        
def addAllcompetitionStandings(leagueID, year):
    db = SessionLocal()

    data = get_api_competition(leagueID, year)

    for team in data:
        t = models.Competitionstanding()
        t.competitionID = leagueID
        t.teamID = team["team"]["id"]
        t.rank = team["rank"]
        t.points = team["points"]
        t.form = team["form"]
        t.description = team["description"]
        t.season = year

        db_team = crud.get_competitionStandings(db, leagueID, t.teamID, year)
        if db_team is not None or (t.competitionID == 61 and t.season == 2010 and t.rank == 20):
            pass
        else:
            db.add(t)
            db.commit()
            print(str(t.competitionID) + " " + str(t.teamID) + " " + str(t.season) + " added to db")
        
        db.close()
        

@router.get("/teampage/{team_id}", response_class=HTMLResponse)
def team_page(request: Request, team_id: int, db: Session = Depends(get_db)):
    data = read_team(team_id, db)
    players =  read_team_players(team_id, db)
    score = teamScore(db, 2021, players)

    overallTeamScore = score["teamScore"]
    weakestArea = score["weakestArea"]
    #stats = read_player_stats(player_id, db)
    
    #title = data["name"]
    return templates.TemplateResponse("team.html", {"request": request, "data": data, "players": players, 'teamScore': overallTeamScore, "weakestArea" : weakestArea})