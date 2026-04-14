FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project files.
COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests

RUN pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -e '.[dev]'

EXPOSE 8000

CMD ["python", "-m", "http.server", "8000"]
