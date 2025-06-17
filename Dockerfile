FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy backend and contracts
COPY ./backend /app
COPY ./contracts /contracts

COPY ./backend/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy backend and contracts
COPY ./backend /app
COPY ./contracts /contracts

COPY ./backend/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
