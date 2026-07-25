FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8080

COPY app ./app

EXPOSE 8080

CMD ["python", "-m", "app"]
