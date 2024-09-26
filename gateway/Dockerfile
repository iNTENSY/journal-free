FROM python:3.11

WORKDIR /gateway

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "src.presentation.entrypoint:app_factory", "--host", "0.0.0.0", "--port", "8000", "--factory"]