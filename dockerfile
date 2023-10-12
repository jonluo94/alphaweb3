FROM python:3.8
ENV PATH /usr/local/bin: $PATH
ADD . /usr/local/alphaweb3
WORKDIR /usr/local/alphaweb3
RUN pip install -r requirements.txt
CMD [ "python", "./cli.py"]
