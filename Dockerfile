# Use the official Python image from the Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Set the environment variable to tell Flask to run in the development environment
ENV FLASK_ENV=development

# Set the environment variable to tell Flask which file is the entry point of the application
ENV FLASK_APP=src/app.py

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

# Expose the port that the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
