FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

COPY consumer/app.py .

CMD ["python", "app.py"]
