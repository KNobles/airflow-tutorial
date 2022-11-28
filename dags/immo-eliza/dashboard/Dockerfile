
FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY dashboard/ /app

# Update pip
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# EXPOSE 8050

#CMD ["python", "main.py"]

CMD ["gunicorn", "main:server"]
