FROM python:3.11.4-slim-bullseye AS prod

WORKDIR /app/src
COPY pyproject.toml poetry.lock /app/src/

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* && \
    pip install poetry==1.4.2 && \
    poetry config virtualenvs.create false && \
    poetry install --only main && \
    apt-get purge -y \
    && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/

CMD ["/usr/local/bin/python", "-m", "pattern"]
