# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN apt-get update \
    && pip install --no-cache-dir --upgrade pip

# Copy the rest of the application code
COPY . .

# Expose the service port
EXPOSE 8001

# Command to run the application
CMD ["python", "app.py"]