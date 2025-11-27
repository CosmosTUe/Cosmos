# Use official Python image as base
FROM python:3.8.18-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    nodejs \
    npm \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Pipenv
RUN pip install pipenv

# Set work directory
WORKDIR /workspace