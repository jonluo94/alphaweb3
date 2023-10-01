FROM python:3.8
ENV PATH /usr/local/bin: $PATH
ADD . /usr/local/myapp/mysite
WORKDIR /usr/local/myapp/mysite
RUN pip install -r requirements.txt
CMD [ "python", "./cli.py"]
