# FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG SLACK_BOT_TOKEN
ARG SLACK_SIGNING_SECRET
ENV SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
ENV SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Hatch
RUN pip install --no-cache-dir hatch

# Copy pyproject.toml and src directory
COPY pyproject.toml .
COPY README.md .
COPY src ./src

# Install project dependencies
# RUN hatch env create

# Go
# CMD ["hatch", "run", "env", "python", "src/social_bot/app.py"]
CMD ["hatch", "run", "env", "uvicorn", "src.social_bot.app:app"]