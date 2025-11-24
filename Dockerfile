FROM python:3.11-slim

WORKDIR /app

# 1. Install Doppler dependencies (gnupg MUST be installed before the Doppler script)
RUN apt-get update && apt-get install -y curl gnupg && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Doppler CLI (MUST be its own RUN block)
RUN curl -Ls https://cli.doppler.com/install.sh | sh

# 3. Ensure Doppler is in PATH
ENV PYTHONPATH="/app/src"
ENV PATH="/usr/local/bin:${PATH}"

# 4. Validate Doppler installation
RUN doppler --version

# 5. Copy requirements first
COPY requirements.txt .

# 6. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy application source
COPY ./src /app/src

EXPOSE 8000

# 8. Run FastAPI using Doppler-managed secrets
CMD ["doppler", "run", "--", "uvicorn", "weather_planner.app:app", "--host", "0.0.0.0", "--port", "8000"]
