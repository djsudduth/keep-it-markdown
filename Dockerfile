FROM ubuntu:22.04
RUN apt update
RUN apt install -y python-is-python3 python3-pip
RUN apt-get install -y curl
RUN apt-get install ca-certificates
RUN curl -L -o tmp/keep-it-markdown-0.6.5.tar.gz https://github.com/djsudduth/keep-it-markdown/archive/refs/tags/0.6.5.tar.gz
RUN tar -zxvf tmp/keep-it-markdown-0.6.5.tar.gz
RUN pip install keyrings.alt
RUN pip install -r /keep-it-markdown-0.6.5/requirements.txt

