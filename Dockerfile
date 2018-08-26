FROM python:2.7-alpine

COPY conv-cidr-changeset.py /bin
COPY requirements.txt /

RUN /bin/sh -c 'pip install -r /requirements.txt; \
pip install awscli'

ENTRYPOINT ["conv-cidr-changeset.py"]
