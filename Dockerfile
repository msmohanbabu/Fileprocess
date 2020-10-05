FROM python:3.8

RUN mkdir /processing
RUN mkdir /processing/file_process
RUN mkdir /processing/test

COPY file_process /processing/file_process
COPY test /processing/test
COPY process_app.py /processing

RUN chmod -R 755 /processing

WORKDIR /processing



