FROM python:3.11-slim-bookworm

WORKDIR /app

COPY container/ .

RUN apt-get update && \
    apt-get install -y python3-pip git curl && \
    pip3 install "git+https://github.com/xchwarze/samsung-tv-ws-api.git#egg=samsungtvws[async,encrypted]" && \
    chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]