FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY engine/ ./engine/

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-m", "engine.ci.pr_reviewer"]