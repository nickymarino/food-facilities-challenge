FROM python:3.9.17-bullseye

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
