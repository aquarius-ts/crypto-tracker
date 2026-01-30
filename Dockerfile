FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY crypto_tracker_simple.py .

# Set display for X11 forwarding (optional)
ENV DISPLAY=:0

# Run the application
CMD ["python", "crypto_tracker_simple.py"]
