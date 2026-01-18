FROM python:3.12-slim

WORKDIR /work

COPY requirements.txt /work/requirements.txt
RUN pip install --no-cache-dir -r /work/requirements.txt

COPY app /work/app
COPY alembic.ini /work/alembic.ini
COPY tests /work/tests
COPY .ruff.toml /work/.ruff.toml