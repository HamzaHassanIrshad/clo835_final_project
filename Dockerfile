# Use lighter image
FROM python:3.9-slim

# Install system packages
RUN apt-get update && \
    apt-get install -y default-mysql-client gcc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create static folder to store background image
RUN mkdir -p /app/static

# Expose port 81 (as per project)
EXPOSE 81

# Run Flask app
ENTRYPOINT ["python3"]
CMD ["app.py"]
