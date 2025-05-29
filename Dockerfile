# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for building packages like tgcrypto
RUN apt-get update && \
    apt-get install -y gcc python3-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file into container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Run the main bot application
CMD ["python", "-m", "bot"]
