# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose the port Railway expects
EXPOSE 8080

# Start the app with Gunicorn
CMD ["gunicorn", "app:application", "--bind", "0.0.0.0:8080"]
