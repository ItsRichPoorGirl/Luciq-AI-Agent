FROM ghcr.io/astral-sh/uv:python3.11-alpine

ENV ENV_MODE production
WORKDIR /app

# Install Python dependencies
COPY backend/pyproject.toml backend/uv.lock ./
ENV UV_LINK_MODE=copy
# Railway doesn't support Docker BuildKit cache mounts, so we use standard uv sync
RUN uv sync --locked --quiet

# Copy application code
COPY backend/ .

# Railway-optimized settings (reduced from production specs)
ENV WORKERS=2
ENV THREADS=2
ENV WORKER_CONNECTIONS=1000

EXPOSE $PORT

# Gunicorn configuration optimized for Railway
CMD ["sh", "-c", "uv run gunicorn api:app \
  --workers $WORKERS \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:$PORT \
  --timeout 1800 \
  --graceful-timeout 600 \
  --keep-alive 1800 \
  --max-requests 0 \
  --max-requests-jitter 0 \
  --forwarded-allow-ips '*' \
  --worker-connections $WORKER_CONNECTIONS \
  --worker-tmp-dir /dev/shm \
  --preload \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  --capture-output \
  --enable-stdio-inheritance \
  --threads $THREADS"] 