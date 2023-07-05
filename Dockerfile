FROM python:3
RUN pip3 install "git+https://github.com/xchwarze/samsung-tv-ws-api.git#egg=samsungtvws[async,encrypted]"
RUN apt-get update && apt-get install -y imagemagick cron

WORKDIR /app
COPY . .

ARG SCHEDULE
ARG MAX_DOWNLOADS
ARG TV_HOST

RUN echo "${SCHEDULE} MAX_DOWNLOADS=${MAX_DOWNLOADS} TV_HOST=${TV_HOST} \
  bash /app/entry.sh >> /var/log/cron.log 2>&1" | crontab -
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
