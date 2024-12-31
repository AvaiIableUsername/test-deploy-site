FROM python:3.12-slim

RUN pip install poetry==1.8.5

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY . .
EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]


