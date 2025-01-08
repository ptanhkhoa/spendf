# Use a Python slim image to minimize the container size
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for SpaCy and other libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    liblzma-dev \
    zlib1g-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SpaCy model (en_core_web_sm)
RUN python -m spacy download en_core_web_sm

# Expose the port that the app will run on
EXPOSE 8080

# Use Gunicorn to run the app in a production environment
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4"]
