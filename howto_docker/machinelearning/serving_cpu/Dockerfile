FROM ubuntu:latest
LABEL maintainer="Jaehong. Kim. <nockchun@gmail.com>"

ENV CONDA_DIR=/opt/conda
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH ${CONDA_DIR}/bin:$PATH
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt update --fix-missing && apt clean && apt update \
 && apt install -y --no-install-recommends wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
        sudo locales fonts-liberation vim net-tools openssh-client graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin \
        autoconf automake dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake \
        libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev \
        libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb \
        libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
        iputils-ping dnsutils language-pack-ko python-opengl ffmpeg openjdk-11-jre-headless libatlas-base-dev libgflags-dev \
        libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libprotobuf-dev libsnappy-dev protobuf-compiler ghostscript python3-tk

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
 && /bin/bash miniconda.sh -f -b -p $CONDA_DIR \
 && rm miniconda.sh \
 && ${CONDA_DIR}/bin/conda clean -tipsy \
 && sudo ln -s ${CONDA_DIR}/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
 && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
 && echo "conda activate base" >> ~/.bashrc \
 && /bin/bash -c "source ~/.bashrc" \
 && conda install -y tini

ADD conda-forge.yml environment.yml
RUN conda env update --name base --file environment.yml \
 && rm environment.yml

EXPOSE 5000
EXPOSE 443
VOLUME /app
VOLUME /data
VOLUME /logs

ENTRYPOINT ["tini", "-g", "--"]

WORKDIR /app