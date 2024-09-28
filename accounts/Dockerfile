FROM python:3.11

WORKDIR /accounts

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "/accounts/src/presentation/entrypoint.py"]