FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY model_training /app
COPY utils/upload_file.py /app/utils/upload_file.py
COPY utils/download_file.py /app/utils/download_file.py

RUN pip3 install -r requirements.txt

CMD [ "python", "main.py" ]