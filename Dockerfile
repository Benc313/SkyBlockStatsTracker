# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for cron
RUN apt-get update && apt-get -y install cron

# Copy the file that lists the python dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Copy the cron job file to the cron directory
COPY crontab /etc/cron.d/skyblock-cron
# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/skyblock-cron
# Apply the cron job
RUN crontab /etc/cron.d/skyblock-cron

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the port the app runs on
EXPOSE 5000

# Run supervisord. This will start both cron and gunicorn (for Flask)
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]