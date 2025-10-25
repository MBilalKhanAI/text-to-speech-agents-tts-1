# TTS Agents Docker Image
# Professional, production-ready container for TTS Agents

FROM python:3.11-slim

# Set metadata
LABEL maintainer="Muhammad Bilal Khan <muhammadbilalkhan@ai.com>"
LABEL description="Professional Text-to-Speech Agents with OpenAI TTS-1"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY examples/ ./examples/
COPY docs/ ./docs/

# Install the package
RUN pip install -e .

# Create non-root user
RUN useradd --create-home --shell /bin/bash tts && \
    chown -R tts:tts /app
USER tts

# Create directories for output
RUN mkdir -p /app/output /app/logs

# Set default environment variables
ENV TTS_OUTPUT_DIR=/app/output
ENV TTS_LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import tts_agents; print('TTS Agents is healthy')" || exit 1

# Expose port (if needed for web interface)
EXPOSE 8000

# Default command
CMD ["python", "-m", "tts_agents.cli", "--help"]
