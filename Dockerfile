FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_lg

# Copy project files
COPY . .

# Create required directories
RUN mkdir -p database resumes

# Expose ports for both services
EXPOSE 8000 8501

# Start script runs both services
CMD ["sh", "start.sh"]
