FROM python:3.7.5

MAINTAINER author="Nélio Rossine de Oliveira"

WORKDIR /code

COPY requirements.txt /code

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD python /code/run.py
