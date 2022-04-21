from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
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

@router.get("/competitions/{competition_id}", response_model=schemas.Competition)
def read_competition(competition_id: int, db: Session = Depends(get_db)):
    db_competition = crud.get_competition(db, competition_id=competition_id)
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    return db_competition
