# Use a slim Python base image
FROM python:3.9-slim

# Install OS-level dependencies
RUN apt-get update && \
    apt-get install -y gcc default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make sure static directory exists
RUN mkdir -p /app/static

# Expose port Flask will run on
EXPOSE 81

# Start the Flask app
CMD ["python3", "app.py"]
