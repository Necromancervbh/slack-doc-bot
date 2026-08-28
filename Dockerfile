FROM python:3.11-slim

LABEL maintainer="Vaibhav Shukla <vaibhavshukl23@gmail.com>"
LABEL description="Slack Doc Bot - AI-powered team assistant using LangChain + Pinecone"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create docs directory if not exists
RUN mkdir -p docs

# Expose port (for future HTTP mode)
EXPOSE 8000

# Default: run the Slack bot
CMD ["python", "-m", "app.bot"]
