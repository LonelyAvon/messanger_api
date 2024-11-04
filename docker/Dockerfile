FROM python:3.12.7-slim-bullseye AS prod

WORKDIR /app/src
COPY pyproject.toml poetry.lock /app/src/

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* && \
    pip install poetry==1.8.2 && \
    poetry config virtualenvs.create false && \
    poetry install --only main && \
    apt-get purge -y \
    && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/

RUN mv .env.deploy .env.develop

CMD ["/usr/local/bin/python", "-m", "pattern"]
