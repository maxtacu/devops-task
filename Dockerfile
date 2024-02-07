FROM python:3.12.2-slim-bullseye

LABEL Maintainer="Maxim Tacu"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./hello_birthday /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]