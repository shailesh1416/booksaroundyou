# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy backend application code
COPY . .

# Expose port for the Flask app
EXPOSE 5000

# Start the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
