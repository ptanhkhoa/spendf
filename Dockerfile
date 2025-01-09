# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git && \
    apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download PhoBERT model
RUN python -c "from transformers import AutoModelForTokenClassification, AutoTokenizer; \
    AutoModelForTokenClassification.from_pretrained('vinai/phobert-large'); \
    AutoTokenizer.from_pretrained('vinai/phobert-large')"

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
