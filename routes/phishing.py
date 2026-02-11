from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.phishing import PhishingAttempt
from database import SessionLocal
import joblib
import os

# ✅ Load ML model safely
model_path = os.path.join(os.path.dirname(__file__), "../phish_detector_v2.joblib")
phishing_model = joblib.load(model_path)

# ✅ Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="templates")


# --- Basic Rule-Based Detector ---
def detect_phishing(content: str) -> str:
    red_flags = [
        "verify your account", "urgent", "click here", "reset your password",
        "update billing info", "login now", "account suspended"
    ]
    score = sum(1 for phrase in red_flags if phrase in content.lower())
    if score >= 2:
        return "⚠️ Likely Phishing"
    elif score == 1:
        return "⚠️ Possibly Suspicious"
    else:
        return "✅ Looks Safe"


# --- Database Session Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ View all logged phishing attempts
@router.get("/attempts", response_class=HTMLResponse)
async def list_attempts(request: Request, db: Session = Depends(get_db)):
    attempts = db.query(PhishingAttempt).order_by(PhishingAttempt.received_at.desc()).all()
    return templates.TemplateResponse("attempts.html", {
        "request": request,
        "attempts": attempts
    })


# ✅ Show the HTML form to submit a new phishing report
@router.get("/submit-form", response_class=HTMLResponse)
def phishing_form(request: Request):
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>PhishSentry | Submit Phishing Report</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

        <style>
            body {
                background-image: url('https://cdn.pixabay.com/photo/2019/11/08/10/34/cyber-4610993_1280.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                color: #e5e7eb;
                font-family: 'Inter', sans-serif;
            }

            .overlay {
                background: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(3px);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 2rem;
            }

            .glow-text {
                color: black;
                text-shadow: 0 0 15px rgba(0,255,150,0.5);
            }

            .btn-cyber {
                background: linear-gradient(90deg, #00ff9d, #00c7ff);
                color: #000;
                padding: 10px 22px;
                border-radius: 6px;
                font-weight: bold;
                transition: all 0.3s ease;
            }

            .btn-cyber:hover {
                transform: scale(1.05);
                box-shadow: 0 0 15px rgba(0,255,150,0.6);
            }

            .card {
                background: rgba(0,0,0,0.75);
                border: 1px solid rgba(0,255,150,0.3);
                border-radius: 12px;
                padding: 2rem;
                box-shadow: 0 0 25px rgba(0,255,150,0.1);
            }

            label {
                color: #9ca3af;
                font-weight: 600;
            }

            input, textarea {
                background-color: rgba(255,255,255,0.1);
                border: 1px solid rgba(0,255,150,0.2);
                color: #e5e7eb;
                border-radius: 6px;
                padding: 8px;
                width: 100%;
            }

            input:focus, textarea:focus {
                outline: none;
                border-color: #00ff9d;
            }
        </style>
    </head>

    <body>
        <div class="overlay">
            <div class="card max-w-xl w-full">
                <h2 class="text-3xl font-extrabold text-green-400 text-center mb-8 glow-text">
                    🚨 Submit a Phishing Report
                </h2>
                
                <form id="phishForm" method="post" action="/submit/">
                    <div class="mb-4">
                        <label>Sender Email</label>
                        <input name="sender" required>
                    </div>
                    <div class="mb-4">
                        <label>Subject</label>
                        <input id="subject" name="subject" required>
                    </div>
                    <div class="mb-6">
                        <label>Email Body Preview</label>
                        <textarea id="content" name="content" required rows="4"></textarea>
                    </div>

                    <div class="flex justify-between mb-4">
                        <button type="button" onclick="scanPhishing()" class="btn-cyber">🔍 Scan Email</button>
                        <button type="submit" class="btn-cyber">✅ Submit Report</button>
                    </div>

                    <div id="scanResult" class="text-lg font-semibold text-green-300 mt-2"></div>
                </form>
            </div>
        </div>

        <script>
        async function scanPhishing() {
            const subject = document.getElementById("subject").value;
            const content = document.getElementById("content").value;
            const formData = new FormData();
            formData.append("subject", subject);
            formData.append("content", content);

            try {
                const response = await fetch("/scan/", { method: "POST", body: formData });
                const data = await response.json();

                const resultDiv = document.getElementById("scanResult");
                resultDiv.textContent = data.verdict || "❌ Error during scan.";
                resultDiv.className = "text-lg font-semibold mt-2";

                if (data.verdict.includes("Safe")) {
                    resultDiv.classList.add("text-green-300");
                } else if (data.verdict.includes("Suspicious")) {
                    resultDiv.classList.add("text-yellow-300");
                } else {
                    resultDiv.classList.add("text-red-400");
                }
            } catch (error) {
                console.error("Scan failed:", error);
                document.getElementById("scanResult").textContent = "❌ Scan failed.";
            }
        }
        </script>
    </body>
    </html>
    """


# ✅ Scan endpoint for AJAX
@router.post("/scan/", response_class=JSONResponse)
async def scan_phishing(subject: str = Form(...), content: str = Form(...)):
    try:
        text_input = f"{subject} {content}"
        prediction = phishing_model.predict([text_input])[0]
        verdict = "⚠️ Likely Phishing" if prediction == 1 else "✅ Looks Safe"
        return {"verdict": verdict}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ✅ Handle form submission and show confirmation page
@router.post("/submit/", response_class=HTMLResponse)
def submit_phishing(
    request: Request,
    sender: str = Form(...),
    subject: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    text_input = f"{subject} {content}"
    prediction = phishing_model.predict([text_input])[0]
    verdict = "Likely Phishing" if prediction == 1 else "Unlikely"

    report = PhishingAttempt(
        sender=sender,
        subject=subject,
        body_preview=content,
        verdict=verdict
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return templates.TemplateResponse("success.html", {
        "request": request,
        "report": report,
        "verdict": verdict
    })
