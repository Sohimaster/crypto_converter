FROM python:3.11
WORKDIR /app

COPY pyproject.toml /app/
RUN pip install -e .
COPY . /app/

ENV PYTHONUNBUFFERED=1
CMD ["python", "src/main.py"]