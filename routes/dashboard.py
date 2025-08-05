from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models.phishing import PhishingAttempt
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def dashboard_view(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/api/attempts-data")
def attempts_data(db: Session = Depends(get_db)):
    attempts = db.query(PhishingAttempt).all()
    data = {
        "labels": [a.timestamp.strftime("%Y-%m-%d %H:%M") for a in attempts],
        "verdicts": [a.verdict for a in attempts]
    }
    return JSONResponse(content=data)
