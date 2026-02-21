FROM python:3.10-slim AS builder

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/python-package -r requirements.txt

COPY . .


FROM python:3.10-slim

WORKDIR /app

# Install runtime libgcc
RUN apt-get update && apt-get install -y \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

## copying only the dependency from builder
COPY --from=builder /python-package /usr/local

## copying as root-user 
COPY . .

## Giving permission manually
RUN chown -R appuser:appgroup /app

## changing as non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
