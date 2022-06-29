FROM pytorch/pytorch:latest

WORKDIR /app

COPY Pipfile Pipfile.lock .

RUN pip install pipenv && \
    pipenv install --system

CMD ["python", "-m", "scripts.generate", "-c", "/configs/config.json"]
