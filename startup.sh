#!/bin/bash

# Exit on any error
set -e

# exporting the project's python's path
export PYTHONPATH=$PWD

# Activate virtual environment
source backend-venv/bin/activate

# Set environment variables from .env file
# export $(grep -v '^#' .env | xargs)


# Start the FastAPI server
echo "Starting FastAPI server..."
# uvicorn app.main:app --reload &

fastapi dev main.py &

# Give FastAPI some time to start
sleep 6

# Start the Celery worker
echo "Starting Celery worker..."
celery -A app.celery_worker.celery_app worker --loglevel=info &

# Start the Celery beat scheduler
echo "Starting Celery beat scheduler..."
celery -A app.celery_worker.celery_app beat --loglevel=info &

# Wait for all background jobs to finish
wait