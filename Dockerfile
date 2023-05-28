FROM python

ENV PYTHONUNBUFFERED 1

WORKDIR /project

COPY requirements.txt /project/

RUN pip install -r requirements.txt
