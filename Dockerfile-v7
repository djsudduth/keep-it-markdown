FROM ubuntu:24.04
RUN apt update
RUN apt install -y python-is-python3 python3-pip
RUN apt-get install -y curl
RUN apt-get install ca-certificates
RUN curl -L -o tmp/keep-it-markdown-0.7.1.tar.gz https://github.com/djsudduth/keep-it-markdown/archive/refs/tags/0.7.1.tar.gz
RUN tar -zxvf tmp/keep-it-markdown-0.7.1.tar.gz
# break-system-packages fine for temporary Docker images - change these to use a venv if running fixed instance 
RUN pip install --break-system-packages keyrings.alt
RUN pip install --break-system-packages -r /keep-it-markdown-0.7.1/requirements.txt

