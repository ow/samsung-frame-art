FROM python:3
RUN pip3 install "git+https://github.com/xchwarze/samsung-tv-ws-api.git#egg=samsungtvws[async,encrypted]"
RUN apt-get install imagemagick

WORKDIR /app
COPY . .

CMD ["./entry.sh"]
