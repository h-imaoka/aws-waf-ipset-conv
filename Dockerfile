FROM python:2.7-alpine

COPY conv-cidr-changeset.py /bin
COPY requirements.txt /
COPY docker-res/direnv /root/.bash_profile

RUN /bin/sh -c 'pip install -r /requirements.txt; \
pip install awscli; \
wget https://github.com/direnv/direnv/releases/download/v2.16.0/direnv.linux-amd64 -O /bin/direnv; \
chmod +x /bin/direnv; \
apk update; \
apk --no-cache add bash'

CMD ["bash", "-l"]
