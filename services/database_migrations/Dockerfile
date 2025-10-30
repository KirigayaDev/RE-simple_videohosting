FROM python:3.12.12-slim

WORKDIR /app/
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENTRYPOINT []

CMD ["alembic", "upgrade", "head"]