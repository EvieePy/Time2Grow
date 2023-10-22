FROM python:3.11

WORKDIR /app

COPY . .

RUN python -m venv venv \
 && . ./venv/bin/activate \
 && pip install -U -r requirements.txt

EXPOSE 8000