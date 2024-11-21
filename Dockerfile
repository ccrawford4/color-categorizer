# Use the official Python image as a base image for linux/amd64
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY app /app

# Expose the FastAPI application port
EXPOSE 8000

# Set the command to run the FastAPI application
# ✅ Do this
CMD ["fastapi", "run", "app.py", "--port", "8000"]