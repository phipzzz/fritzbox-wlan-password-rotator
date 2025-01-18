FROM python:3-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG VERSION="unknown"

RUN echo "$VERSION" > /app/version.txt

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]