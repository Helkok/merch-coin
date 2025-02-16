FROM python:3.12-slim

COPY app /work/app
COPY requirements.txt /work
COPY alembic.ini /work
COPY .ruff.toml /work
COPY alembic.ini /work
COPY tests /work/tests

WORKDIR /work

RUN pip install --no-cache-dir --upgrade -r requirements.txt