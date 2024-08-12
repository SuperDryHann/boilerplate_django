# Use the official Python image from Docker Hub
FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git && apt-get clean
RUN git config --global user.email "han@askhomer.ai" \
    && git config --global user.name "SuperDryHann"

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Run collectstatic
# RUN python manage.py collectstatic --noinput

# Expose port 8000 for the application
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "azureproject.wsgi:application"]


