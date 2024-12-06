# Use Python as the base image
FROM python:3.11.11-alpine3.19

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ /app/

# Expose the Flask app port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "main.py"]