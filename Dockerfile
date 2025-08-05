# 🔧 Use Python base image
FROM python:3.11-slim

# 📁 Set working directory
WORKDIR /app

# 🚀 Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# 📦 Copy local dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📁 Copy all project files
COPY . .

# 🌍 Expose FastAPI port
EXPOSE 8000

# 🏁 Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
