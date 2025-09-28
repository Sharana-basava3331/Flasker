# Use official Python runtime as base
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the port Flask/Gunicorn will run on
EXPOSE 5000

# Start the app with Gunicorn (production-ready WSGI server)
CMD ["gunicorn", "index:app", "-b", "0.0.0.0:5000"]
