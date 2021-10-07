FROM python:3.9

# useful to get log
ENV PYTHONUNBUFFERRED 1 

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt 

# copy everything from admin
COPY . /app

# CMD python3 consumer.py