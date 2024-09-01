FROM python:latest AS build

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

FROM python:slim AS production

# Set the working directory in the container
WORKDIR /app

# Copy the .env file into the container
COPY --from=build /app/.env .env

# Copy the installed dependencies and application code from the build stage
COPY --from=build /app /app

# Set environment variables
ENV FLASK_ENV=development
ENV FLASK_APP=src/app.py
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app"

# Expose the port that the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
