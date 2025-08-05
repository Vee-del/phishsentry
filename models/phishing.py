from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
from datetime import datetime
from .base import Base

class PhishingAttempt(Base):
    __tablename__ = "phishing_attempts"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    subject = Column(String)
    body_preview = Column(String)
    verdict = Column(String)
    received_at = Column(DateTime, default=datetime.utcnow)
