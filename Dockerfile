FROM python:3.8

WORKDIR /

COPY file_process/ .
COPY test/ .
ADD process_app.py .

ENTRYPOINT ["python3", "process_app.py"]

