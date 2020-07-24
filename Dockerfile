FROM python:3.8.2-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install gunicorn
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Create directory structure for testing the IFS
RUN mkdir -p /tmp/testdir/a1/b/c/d /tmp/testdir/a2 /tmp/testdir/a3 && \
    touch /tmp/testdir/f1 /tmp/testdir/f2 /tmp/testdir/f3 /tmp/testdir/a1/f1

# copy project
COPY . /app/

RUN echo "BASE_PATH = '/tmp/testdir'" >> /app/settings.cfg

ENTRYPOINT gunicorn --chdir /app webapp:app -w 2 --threads 2 -b 0.0.0.0:5000