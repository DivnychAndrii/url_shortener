FROM python:3.9-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN apt-get update \
    && apt-get install gcc libpq-dev -y

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --deploy --system

COPY source ./source
COPY alembic_migrations ./alembic_migrations
COPY tests ./tests
COPY main.py ./main.py

ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]