FROM python:3

MAINTAINER Troy Caro "twc17@pitt.edu"

ENV TZ America/New_York

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./get_console.py" ]
