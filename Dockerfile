# Simple Dockerfile for the Flask Quiz app
FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Expose port (Koyeb overrides this, kept for local fallback)
EXPOSE 5000

# Run using gunicorn for production (Uses shell form to evaluate PORT env var)
CMD gunicorn main:app -b 0.0.0.0:${PORT:-5000} --workers 3
