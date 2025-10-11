# Use the official Python image
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
 

# Install system dependencies required for Pillow and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    tk-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy application code and supervisor config
COPY . . 

# Make scripts executable
RUN chmod +x /app/scripts.sh

# Expose the necessary port
EXPOSE 8000
EXPOSE 8001



