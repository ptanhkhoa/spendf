# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies (this layer will be cached if requirements.txt doesn't change)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (this layer changes only when app files are updated)
COPY . .

# Expose the port your app will run on
EXPOSE 8080

# Set the command to run your app using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
