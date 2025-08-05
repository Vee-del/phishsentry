from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.phishing import PhishingAttempt
from database import SessionLocal
import joblib
import os

# Load ML model
model_path = os.path.join(os.path.dirname(__file__), "../phish_detector.joblib")
phishing_model = joblib.load('phish_detector_v2.joblib')

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

# DB session handler
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ View all logged phishing attempts
@router.get("/attempts", response_class=HTMLResponse)
def list_phishing_attempts(request: Request, db: Session = Depends(get_db)):
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
        <title>Submit Phishing Report</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            .bg-cyber {
                background-image: url('https://cdn.pixabay.com/photo/2019/11/08/10/34/cyber-4610993_1280.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            .bg-overlay {
                background-color: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(3px);
            }
            .glow-text {
                text-shadow: 0 0 10px rgba(0,255,150,0.8);
            }
            .btn {
                transition: all 0.3s ease;
            }
            .btn:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 14px rgba(0,255,150,0.5);
            }
        </style>
    </head>
    <body class="bg-cyber min-h-screen flex items-center justify-center text-white">
        <div class="bg-overlay max-w-xl w-full p-8 rounded shadow-lg">
            <h2 class="text-3xl font-extrabold text-green-400 text-center mb-6 glow-text"> Report a Phishing Attempt</h2>
<form id="phishForm" method="post" action="/submit/">
    <div class="mb-4">
        <label class="block text-sm font-medium text-gray-200">Sender Email</label>
        <input name="sender" required class="mt-1 block w-full border border-gray-500 bg-gray-800 text-white rounded p-2">
    </div>
    <div class="mb-4">
        <label class="block text-sm font-medium text-gray-200">Subject</label>
        <input id="subject" name="subject" required class="mt-1 block w-full border border-gray-500 bg-gray-800 text-white rounded p-2">
    </div>
    <div class="mb-6">
        <label class="block text-sm font-medium text-gray-200">Email Body Preview</label>
        <textarea id="content" name="content" required rows="4" class="mt-1 block w-full border border-gray-500 bg-gray-800 text-white rounded p-2"></textarea>
    </div>

    <!-- 🔍 Scan Button -->
    <div class="flex justify-between mb-4">
        <button type="button" onclick="scanPhishing()" class="btn bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded">
            🔍 Scan Email
        </button>
        <button type="submit" class="btn bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded">
            ✅ Submit Report
        </button>
    </div>

    <!-- 🧠 Verdict Display -->
    <div id="scanResult" class="text-lg font-semibold text-green-300 mt-2"></div>
</form>

        </div>
<script>
async function scanPhishing() {
    const subject = document.getElementById("subject").value;
    const content = document.getElementById("content").value;

    const formData = new FormData();
    formData.append("subject", subject);
    formData.append("content", content);

    try {
        const response = await fetch("/scan/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        const resultDiv = document.getElementById("scanResult");
        resultDiv.textContent = data.verdict || "❌ Error during scan.";
        resultDiv.classList.remove("text-green-300", "text-yellow-300", "text-red-300");

        if (data.verdict.includes("Safe")) {
            resultDiv.classList.add("text-green-300");
        } else if (data.verdict.includes("Suspicious")) {
            resultDiv.classList.add("text-yellow-300");
        } else {
            resultDiv.classList.add("text-red-300");
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

@router.post("/scan/", response_class=JSONResponse)
async def scan_phishing(subject: str = Form(...), content: str = Form(...)):
    try:
        text_input = f"{subject} {content}"
        prediction = phishing_model.predict([text_input])[0]
        verdict = "⚠ Likely Phishing" if prediction == 1 else "✅ Looks Safe"
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
    # 📊 Predict using the ML model
    text_input = f"{subject} {content}"
    prediction = phishing_model.predict([text_input])[0]
    verdict = "Likely Phishing" if prediction == 1 else "Unlikely"

    # 💾 Store in the DB including verdict
    report = PhishingAttempt(
        sender=sender,
        subject=subject,
        body_preview=content,
        verdict=verdict  # ✅ Save this in the DB
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    # ✅ Pass verdict to the template
    return templates.TemplateResponse("success.html", {
        "request": request,
        "report": report,
        "verdict": verdict
    })
