FROM python:3.11.11-slim

# Set working directory
WORKDIR /app

# Install dependencies directly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Run the application with hot reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload", "--reload-dir", "/app"]
