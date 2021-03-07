FROM python:3.6
RUN mkdir -p /usr/ev_demo
WORKDIR /usr/ev_demo

COPY . /usr/ev_demo

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements

RUN alias python=python3
CMD ["./run.sh"];
