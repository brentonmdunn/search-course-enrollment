FROM python:latest


COPY . /usr/app/src/
WORKDIR /usr/app/src

CMD [ "python", "./main.py"]
