# Use the official Python image as a base image
FROM python:3.10-slim

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
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]