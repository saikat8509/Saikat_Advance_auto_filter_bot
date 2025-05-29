FROM python:3.10-slim

WORKDIR /app

# Install build tools and dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project (including bot/, config/, etc.)
COPY . /app/

# Launch the bot module
CMD ["python", "-m", "bot"]
