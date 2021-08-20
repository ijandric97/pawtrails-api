FROM python:3.8-slim-buster

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
# Turns off buffering for easier container logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install poetry
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy and install the requirements
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev

# Copy the application
WORKDIR /pawtrails
COPY . /pawtrails

# Creates a non-root user with an explicit UID and adds permission to access the /pawtrails folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /pawtrails
USER appuser

# During debugging, this entry point will be overridden.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "pawtrails.main:app"]
