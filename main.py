from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from database import engine
from models import Base
from routes import phishing, dashboard

app = FastAPI(title="PhishSentry | AI-Powered Phishing Defense")

Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(phishing.router)
app.include_router(dashboard.router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>PhishSentry | AI-Powered Phishing Detection</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #020617;
                color: #e5e7eb;
            }
            .hero-bg {
                background: radial-gradient(circle at 20% 30%, rgba(0,255,200,0.15) 0%, transparent 80%),
                            radial-gradient(circle at 80% 70%, rgba(0,255,150,0.2) 0%, transparent 70%);
            }
            .glow-text {
                text-shadow: 0 0 15px rgba(0,255,150,0.8);
            }
            .btn-cyber {
                background: linear-gradient(90deg, #00ff9d, #00c7ff);
                color: #000;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            .btn-cyber:hover {
                transform: scale(1.07);
                box-shadow: 0 0 15px rgba(0,255,150,0.7);
            }
            .terminal-box {
                background: rgba(0, 0, 0, 0.7);
                border: 1px solid rgba(0,255,150,0.3);
                border-radius: 10px;
                padding: 20px;
                font-family: monospace;
                color: #00ff9d;
                overflow: hidden;
                box-shadow: 0 0 20px rgba(0,255,150,0.1);
            }
            .blink {
                animation: blink 1s step-start infinite;
            }
            @keyframes blink {
                50% { opacity: 0; }
            }
        </style>
    </head>

    <body class="hero-bg min-h-screen flex flex-col items-center justify-center text-center px-6">
        <header class="mb-10">
            <h1 class="text-6xl font-extrabold text-green-400 glow-text">PhishSentry</h1>
            <p class="text-gray-300 text-lg mt-3">AI-Powered. Real-Time. Cyber-Ready.</p>
        </header>

        <main class="max-w-3xl space-y-6">
            <div class="terminal-box text-left">
                <p>> Initializing defense protocols...</p>
                <p>> Scanning for suspicious payloads...</p>
                <p>> <span class="text-green-400">System Secure ✅</span></p>
                <p>> Ready to intercept phishing attempts<span class="blink">|</span></p>
            </div>

            <div class="mt-8 flex flex-wrap justify-center gap-4">
                <a href="/submit-form" class="btn-cyber">🚨 Report Phishing</a>
                <a href="/attempts" class="btn-cyber">📋 View Attempts</a>
                <a href="/dashboard" class="btn-cyber">📊 Analytics Dashboard</a>
            </div>
        </main>

        <footer class="mt-16 text-sm text-gray-500">
            © 2025 PhishSentry — Securing the Web, One Email at a Time.
        </footer>
    </body>
    </html>
    """
