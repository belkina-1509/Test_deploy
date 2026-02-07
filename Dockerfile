FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    APP_DATABASE=/data/test.db \
    APP_LOG_LEVEL=INFO

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY utils.py /app/utils.py

VOLUME ["/data"]

CMD ["python", "utils.py"]
