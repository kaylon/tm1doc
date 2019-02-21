FROM python:3.6-alpine



# build utils - remove these after
RUN apk add --update \
  gcc \
  python3-dev \
  curl \
  linux-headers \
  graphviz \
  make \
  g++ \
  subversion


run python3 -m ensurepip && \
  pip3 install --no-cache-dir --upgrade pip setuptools

WORKDIR /srv/app

Add . /srv/app


run pip3 install --no-cache-dir --upgrade -r requirements.txt

RUN rm -rf \
    /var/lib/apt/lists/* \
    /tmp/* \
    /var/tmp/* \
    /usr/share/man \
    /usr/share/doc \
    /usr/share/doc-base


# RUN apk remove \
#   gcc \
#   python3-dev \
#   musl-dev \
#   linux-headers

CMD ["/bin/bash"]
