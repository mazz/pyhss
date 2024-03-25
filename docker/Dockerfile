FROM ubuntu:focal as builder
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/open5gs/install/lib/x86_64-linux-gnu
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip python3-dev\
        python3-setuptools \
        python3-wheel \
        ninja-build \
        build-essential \
        flex \
        bison \
        git \
        libsctp-dev \
        libgnutls28-dev \
        libgcrypt-dev \
        libssl-dev \
        libidn11-dev \
        libmongoc-dev \
        libbson-dev \
        libyaml-dev \
        meson \
        mongodb \
        curl \
        gnupg \
        ca-certificates \
        libmicrohttpd-dev \
        libcurl4-gnutls-dev \
        libnghttp2-dev \
        libtins-dev \
        libidn11-dev \
        libtalloc-dev \
        libpq-dev \
        libmysqlclient-dev \
        libsystemd-dev \
        python3-psycopg2 \
        vim \
        tcpdump \
        redis-server

# RUN git clone https://github.com/mazz/pyhss.git
RUN git clone --single-branch --branch env-changes https://github.com/mazz/pyhss.git
WORKDIR pyhss
COPY config.yaml ./
COPY *.sh ./
RUN mkdir -p log
RUN pip3 install -r requirements.txt

RUN cp /pyhss/tools/Diameter_client.py /pyhss/

RUN cp /pyhss/lib/banners.py /pyhss/
RUN cp /pyhss/lib/CryptoTool.py /pyhss/
RUN cp /pyhss/lib/database.py /pyhss/
RUN cp /pyhss/lib/diameter.py /pyhss/
RUN cp /pyhss/lib/diameterAsync.py /pyhss/
RUN cp /pyhss/lib/logtool.py /pyhss/
RUN cp /pyhss/lib/lte.py /pyhss/
RUN cp /pyhss/lib/messaging.py /pyhss/
RUN cp /pyhss/lib/messagingAsync.py /pyhss/
RUN cp /pyhss/lib/metrics.py /pyhss/
RUN cp /pyhss/lib/milenage.py /pyhss/
RUN cp /pyhss/lib/mongodb_insert_subscriber.py /pyhss/
RUN cp /pyhss/lib/S6a_crypt.py /pyhss/

RUN cp /pyhss/services/hssService.py /pyhss/
RUN cp /pyhss/services/apiService.py /pyhss/
RUN cp /pyhss/services/databaseService.py /pyhss/
RUN cp /pyhss/services/diameterService.py /pyhss/
RUN cp /pyhss/services/georedService.py /pyhss/
RUN cp /pyhss/services/logService.py /pyhss/
RUN cp /pyhss/services/metricService.py /pyhss/

RUN chmod +x *.sh

ENTRYPOINT [ "/pyhss/entrypoint.sh" ]
CMD [ "/usr/bin/python3", "hssService.py" ] 
