from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.db import SessionLocal
from sqlalchemy.orm import Session

from app.db import schemas, crud

from app.services.apifootball import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
templates = Jinja2Templates(directory="templates")

@router.get("/competitions/{competition_id}", response_model=schemas.Competition)
def read_competition(competition_id: int, db: Session = Depends(get_db)):
    db_competition = crud.get_competition(db, competition_id=competition_id)
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    return db_competition

@router.get("/competitionstandings/{competition_id}")
def read_competitionstandings(competition_id: int, db: Session = Depends(get_db), season : Optional[int] = 2021):
    db_competition = crud.get_competitionStandings(db, competition_id, season)
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    return db_competition

@router.get("/competitionpage/", response_class=HTMLResponse)
def competition_page(request: Request, competition_id: int, season : Optional[int] = 2021, db: Session = Depends(get_db)):
    data =  read_competition(competition_id, db)
    standings = read_competitionstandings(competition_id, db, season)

    return templates.TemplateResponse("competition.html", {"request": request, "data": data, 'standings': standings})