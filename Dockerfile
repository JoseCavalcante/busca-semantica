
# Stage 1: Builder (Compile dependencies)
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies required for building python packages (like psycopg2, fitz)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into a temporary location
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (Minimal image)
FROM python:3.11-slim

WORKDIR /app

# Install runtime system dependencies (libpq for postgres)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /root/.local /root/.local

# Ensure scripts (like uvicorn) are in PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run commands
# We use shell form to allow variable expansion if needed, but array is safer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
