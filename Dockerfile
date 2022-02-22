FROM python:3.9

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./routing /app/routing

CMD ["uvicorn", "routing.api:app", "--host", "0.0.0.0", "--port", "80"]

