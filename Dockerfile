# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy everything into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (optional, use .env in production)
ENV PYTHONUNBUFFERED=1

# Run the bot using bot/main.py
CMD ["python", "bot/main.py"]
