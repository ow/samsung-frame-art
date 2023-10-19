ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
  build-base \
  python3-dev \
  libffi-dev \
  git \
  imagemagick \
  font-dejavu

RUN pip install "git+https://github.com/xchwarze/samsung-tv-ws-api.git#egg=samsungtvws[async,encrypted]"

WORKDIR /app
COPY . .

ARG SCHEDULE
ARG MAX_DOWNLOADS
ARG TV_HOST

RUN echo "${SCHEDULE} MAX_DOWNLOADS=${MAX_DOWNLOADS} TV_HOST=${TV_HOST} bash /app/entry.sh" >> /var/spool/cron/crontabs/root

CMD date && crond -f -L /dev/stdout
