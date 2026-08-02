FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL="sqlite:////app/data/lordsahu.db"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies manifest and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create volume directory for persistent SQLite storage
RUN mkdir -p /app/data

# Copy backend source code
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
