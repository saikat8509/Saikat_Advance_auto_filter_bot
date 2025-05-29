# Use official slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build tools (gcc, etc.) for compiling dependencies like tgcrypto
RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH so modules can be resolved correctly
ENV PYTHONPATH=/app

# Run the main module
CMD ["python", "-m", "bot.main"]
