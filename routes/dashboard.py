from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from database import SessionLocal
from models.phishing import PhishingAttempt

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard", response_class=HTMLResponse)
def render_dashboard(request: Request):
    """Renders the main analytics dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/api/attempts-data")
def attempts_data(db: Session = Depends(get_db)):
    """Aggregated attempt data for Chart.js"""
    now = datetime.utcnow()
    start = now - timedelta(hours=24)
    rows = (
        db.query(
            func.date_trunc('hour', PhishingAttempt.received_at).label('bucket'),
            func.count(PhishingAttempt.id).label('count')
        )
        .filter(PhishingAttempt.received_at >= start)
        .group_by('bucket')
        .order_by('bucket')
        .all()
    )

    series = [{"bucket": r.bucket.isoformat(), "count": r.count} for r in rows]
    total = db.query(func.count(PhishingAttempt.id)).scalar() or 0
    last_24 = sum(r["count"] for r in series)

    return {
        "series": series,
        "summary": {
            "total_attempts": total,
            "last_24h": last_24
        }
    }


@router.get("/api/recent-attempts")
def recent_attempts(db: Session = Depends(get_db)):
    """Fetches latest 10 attempts"""
    records = (
        db.query(PhishingAttempt)
        .order_by(desc(PhishingAttempt.received_at))
        .limit(10)
        .all()
    )

    data = [
        {
            "id": r.id,
            "sender": r.sender,
            "subject": r.subject,
            "verdict": r.verdict,
            "received_at": r.received_at.isoformat(),
        }
        for r in records
    ]
    return JSONResponse(content=data)
