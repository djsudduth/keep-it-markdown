FROM python:3.13-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -L -o tmp/keep-it-markdown-0.8.0.tar.gz https://github.com/djsudduth/keep-it-markdown/archive/refs/tags/0.8.0.tar.gz \
    && tar -zxvf tmp/keep-it-markdown-0.8.0.tar.gz \
    && rm tmp/keep-it-markdown-0.8.0.tar.gz

RUN pip install keyrings.alt
RUN pip install /keep-it-markdown-0.8.0
WORKDIR /keep-it-markdown-0.8.0