# Use a Python slim image to minimize the container size
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install SpaCy model (en_core_web_sm)
RUN python -m spacy download en_core_web_sm

# Expose the port that the app will run on
EXPOSE 8080

# Use Gunicorn to run the app in a production environment
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4"]
