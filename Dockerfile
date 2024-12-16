# Use Python 3.11 as base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the necessary ports for the server and client

# For gRPC server
EXPOSE 50051  
# For HTTP server (aiohttp)
EXPOSE 8000   

# Command to start the server
CMD ["python", "app.py"]
