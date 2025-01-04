if [ -z "$PORT" ]; then
  # If PORT is not set, assume it's local development
  echo "Running in local development mode..."
  uvicorn main:app --host 0.0.0.0 --port 5000 --reload
else
  # If PORT is set, assume it's Heroku or production
  echo "Running in development mode on port $PORT..."
  uvicorn main:app --host 0.0.0.0 --port $PORT
fi