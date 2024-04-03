FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install -e .
ENV PYTHONUNBUFFERED=1
CMD ["python", "src/main.py"]