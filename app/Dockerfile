FROM python:3.11-slim-bullseye

WORKDIR /usr/src/app
COPY ../requirements.txt ./
RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT /usr/src/app/docker-entrypoint.sh
