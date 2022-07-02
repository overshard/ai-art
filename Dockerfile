FROM pytorch/pytorch:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
      git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Pipfile Pipfile.lock .
RUN pip install pipenv && \
    pipenv install --system

COPY scripts scripts
COPY core core

VOLUME /data

CMD ["python", "-m", "scripts.generate", "-c", "/data/config.json"]
