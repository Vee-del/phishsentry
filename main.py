from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from database import engine
from routes import phishing, dashboard
from models import Base

app = FastAPI(title="PhishSentry API")

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
        <meta charset="UTF-8">
        <title>PhishSentry | Home</title>
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
                background-color: rgba(0, 0, 0, 0);
                backdrop-filter: blur(0px);
            }
            .glow-text {
                text-shadow: 0 0 10px rgba(0,255,150,0.8);
            }
            .ripple-btn {
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
            }
            .ripple-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 14px rgba(0,255,150,0.5);
            }
            .ripple-effect {
                position: absolute;
                border-radius: 50%;
                transform: scale(0);
                animation: ripple-animation 0.6s linear;
                background-color: rgba(255, 255, 255, 0.7);
                pointer-events: none;
            }
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        </style>
    </head>
    <body class="bg-cyber min-h-screen text-white">
        <div class="bg-overlay min-h-screen flex items-center justify-center px-6 py-10">
            <div class="max-w-6xl w-full grid md:grid-cols-2 gap-10 items-center bg-black bg-opacity-70 p-10 rounded-xl shadow-lg">
                
                <!-- Left Content -->
                <div>
                    <h1 class="text-5xl font-extrabold text-green-400 glow-text mb-6">🛡 PhishSentry</h1>
                    <p class="text-lg text-gray-200 mb-4">
                        A modern tool to detect, log, and defend against phishing attempts in real time.
                        Your digital firewall — fast, transparent, and built for the modern web.
                    </p>
                    <ul class="list-disc list-inside text-gray-300 mb-6">
                        <li>🚨 Real-time phishing reports</li>
                        <li>📈 Visualized attack logs</li>
                        <li>🧠 Easy-to-use interface, no clutter</li>
                    </ul>
                    <div class="space-x-4">
                        <a href="/submit-form" class="ripple-btn inline-block bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-full relative overflow-hidden">
                            Report Phishing
                        </a>
                        <a href="/attempts" class="ripple-btn inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-full relative overflow-hidden">
                            View Attempts
                        </a>

                    </div>
                    <a href="/dashboard" class="ripple-btn inline-block bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded shadow">
    📊 View Dashboard
</a>

                </div>

                <!-- Right Visual -->
                <div class="hidden md:block">
                    <img src="https://cdn.pixabay.com/photo/2017/10/10/21/48/security-2838923_1280.jpg" alt="PhishSentry Interface" class="rounded-lg shadow-xl">
                </div>
            </div>
        </div>

        <script>
            document.querySelectorAll('.ripple-btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    const circle = document.createElement('span');
                    circle.classList.add('ripple-effect');
                    const diameter = Math.max(this.clientWidth, this.clientHeight);
                    circle.style.width = circle.style.height = `${diameter}px`;
                    circle.style.left = `${e.offsetX - diameter / 2}px`;
                    circle.style.top = `${e.offsetY - diameter / 2}px`;
                    this.appendChild(circle);
                    setTimeout(() => circle.remove(), 600);
                });
            });
        </script>
    </body>
    </html>
    """

