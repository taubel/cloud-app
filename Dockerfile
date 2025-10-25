FROM python:3.13-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY . .
RUN pip install .

RUN useradd app
USER app

CMD ["python", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "cloud_app.app:app"]
