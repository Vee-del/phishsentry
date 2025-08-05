from models.phishing import PhishingAttempt
from database import SessionLocal

# Create a new database session
db = SessionLocal()

# Add a dummy phishing attempt
dummy_attempt = PhishingAttempt(
    sender="malicious@fakebank.com",
    subject="Urgent: Account Suspended!",
    body_preview="Click this link to verify your account..."
)

# Add and commit to database
db.add(dummy_attempt)
db.commit()
db.close()

print("✅ Dummy phishing attempt added successfully.")
