# Use it with:
#  $ docker build -t autobx .
#  $ docker run -p5000:5000 autobx

FROM python:3

WORKDIR /

ADD src src

EXPOSE 5000

RUN pip3 install flask

CMD python3 src/autobox.py
