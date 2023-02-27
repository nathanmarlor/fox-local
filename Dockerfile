FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /src .

EXPOSE 10001

CMD [ "python3", "fox-local.py"]
