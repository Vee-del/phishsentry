# 🛡️ PhishSentry

PhishSentry is a lightweight, AI-powered phishing detection system built with **FastAPI**, **PostgreSQL**, and styled using **Tailwind CSS**. Designed to empower digital security across East Africa and beyond, it provides a clean UI and smart backend capable of evaluating email reports for phishing indicators.

---

## 🚀 Features

- Real-time phishing detection
- Machine learning-based verdict engine (using scikit-learn)
- Clean Tailwind CSS frontend
- RESTful FastAPI backend
- PostgreSQL database with structured verdict logging
- Docker + Firebase-ready for cloud deployment

---

## 🧪 Tech Stack

| Layer         | Stack                          |
|--------------|-------------------------------|
| Frontend      | Tailwind CSS                  |
| Backend       | FastAPI + Python              |
| Database      | PostgreSQL                    |
| ML Models     | Scikit-learn (joblib)         |
| Deployment    | Docker + Firebase Hosting     |

---

## 🛠️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/phishsentry.git
cd phishsentry

# Activate your virtualenv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
