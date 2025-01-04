FROM python:3.11.11-alpine3.19

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY /app . 

RUN chmod +x start.sh

CMD ["sh", "./start.sh"]
