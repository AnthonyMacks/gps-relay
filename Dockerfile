# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code into the container
COPY . .

# Expose the port your app runs on (Fly uses 3000 by default)
ENV PORT=3000
EXPOSE 3000

# Run the Flask app
CMD ["python", "gps-relay.py"]
