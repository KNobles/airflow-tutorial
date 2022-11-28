FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY scraper /app
COPY utils/upload_file.py /app/utils/upload_file.py

RUN apt update -y
RUN apt install firefox-esr -y
RUN pip3 install -r /app/requirements.txt

CMD [ "python", "main.py" ]