FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DATABASE_HOST db
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

