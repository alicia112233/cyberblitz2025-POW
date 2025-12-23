# Dockerfile
# this is gpt'd sorry i can't be bothered
FROM python:3.11-slim AS builder

WORKDIR /app

COPY . .
RUN chown root:root ./flagreader && chmod 0111 ./flagreader

FROM python:3.11-slim

WORKDIR /app

RUN useradd --create-home --shell /bin/bash pwnscope

COPY --from=builder /app /app

RUN chown root:root /app/flagreader \
    && chmod 0111 /app/flagreader \
    && chmod -R go-w /app

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

USER pwnscope
RUN pip install flask
CMD ["python", "app.py"]

