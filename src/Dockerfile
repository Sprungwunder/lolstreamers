# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=lolstreamers.settings
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PYTHONPATH=/app/src

# Create and set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create poetry cache directory and set permissions
RUN mkdir -p $POETRY_CACHE_DIR && chmod 777 $POETRY_CACHE_DIR

# Create directory for certificates
RUN mkdir -p /app/certs


# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copy poetry configuration files
COPY poetry.lock pyproject.toml ./

# Configure poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy project
COPY . /app/

# Install the project itself
RUN poetry install --no-interaction --no-ansi

# Create and switch to non-root user
RUN useradd -m django
RUN chown -R django:django /app
RUN chown -R django:django $POETRY_CACHE_DIR

# Create static files directory with correct permissions
RUN mkdir -p /app/src/lolstreamers/staticfiles
RUN chown -R django:django /app/src/lolstreamers/staticfiles

# Collect static files
RUN cd src && poetry run python manage.py collectstatic --noinput

#RUN ls -al /app/src/lolstreamers/staticfiles

USER django

# Expose the port the app runs on
EXPOSE 8000

# Start Gunicorn
CMD ["poetry", "run", "gunicorn", "--chdir", "src", "--bind", "0.0.0.0:8000", "lolstreamers.wsgi:application", "--workers", "3"]
