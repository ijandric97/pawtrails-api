# NOTE: Do not use Alpine for python, it will fail since no GCCs
FROM python:3.8-slim

COPY pyproject.toml .

RUN python -m pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
