from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import null
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.db import SessionLocal
from sqlalchemy.orm import Session

from app.db import schemas, crud, models
from app.library.algorithms import teamScore, compareTeamStats, teamWinChance

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

@router.get("/teams/stats/{team_id}", response_model=schemas.Teamstats)
def read_team_stats(team_id: int, db: Session = Depends(get_db), season : Optional[int] = 2021):
    db_team = crud.get_team_stats(db, team_id=team_id, season=season)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team stats not found for season " + str(season))
    return db_team

@router.get("/teamcompetition/{team_id}")
def read_team_competition(team_id: int, db: Session = Depends(get_db), season : Optional[int] = 2021):
    db_team = crud.get_team_competition_details(db, team_id, season)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team[0]

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
    return templates.TemplateResponse(
        "search.html", {"request": request, "teams": teams}
    )

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
        

@router.get("/teampage/", response_class=HTMLResponse)
def team_page(request: Request, team_id: int, season : Optional[int] = 2021, db: Session = Depends(get_db)):
    data = read_team(team_id, db)
    stats = read_team_stats(team_id, db, season)
    players =  read_team_players(team_id, db)
    leagueDetails = read_team_competition(team_id, db, season)
    score = teamScore(db, season, players)

    overallTeamScore = score["teamScore"]
    weakestArea = score["weakestArea"]

    return templates.TemplateResponse("team.html", {"request": request, "data": data, "stats": stats, "players": players, "leagueDetails": leagueDetails, 'teamScore': overallTeamScore, "weakestArea" : weakestArea})

@router.get("/compareteams")
def compare_teams(request: Request, query: int, team_id: int, db: Session = Depends(get_db)):
    team1 = read_team(team_id, db)
    team2 = read_team(query, db)
    players1 =  read_team_players(team_id, db)
    players2 =  read_team_players(query, db)

    scores = compareTeamStats(db, 2021, players1, players2)

    team1Score = scores["team1Score"]
    team2Score = scores["team2Score"]
    team1Weakness = scores["team1Weakness"]
    team2Weakness = scores["team2Weakness"]
    similarity = scores["similarity"]

    homeTeamWin = round(teamWinChance(team1Score/100, team2Score/100), 1)
    awayTeamWin = round(100 - homeTeamWin, 1)
    

    print(team1Score, team2Score, homeTeamWin)

    #params = request.query_params
    #if player2 is None or player1 is None:
        #raise HTTPException(status_code=404, detail="Player not found")
    return templates.TemplateResponse(
        "teamcompare.html", {"request": request, "team1": team1, "team1Score": team1Score, "team1Weakness": team1Weakness, "team2": team2, "team2Score": team2Score, "team2Weakness": team2Weakness, "similarity": similarity, "homeTeamWin": homeTeamWin, "awayTeamWin": awayTeamWin}
    )
