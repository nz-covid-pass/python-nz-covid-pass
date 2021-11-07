### Dockerfile for nz-covid-pass-verifier

# Plpine POS 3.8
FROM python:alpine

RUN set -x \
    && apk add --no-cache gcc py3-cffi libc-dev jpeg-dev libffi-dev zbar-dev \
    && rm -rf /var/cache/apk/*

#RUN set -x \
#    && apk add --no-cache ython2-dev py2-openssl python3 \
#    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . .

RUN set -x \
     && pip install -r requirements.txt


ENTRYPOINT ["python3", "nz_covid_pass_verifier.py"]
#ENTRYPOINT /bin/sh
#CMD /bin/sh

