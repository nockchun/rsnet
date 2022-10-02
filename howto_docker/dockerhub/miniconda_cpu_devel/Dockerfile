FROM ubuntu:22.04
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

# Install system packages
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TZ=Asia/Seoul
ARG DEBIAN_FRONTEND=noninteractive
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt-get update --fix-missing \
 && apt-get upgrade -y \
 && apt-get install -yq --no-install-recommends debconf apt-utils apt wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
    sudo locales fonts-liberation vim net-tools openssh-client graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin \
    autoconf automake dpkg-dev file build-essential g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake \
    libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev \
    libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb \
    libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
    iputils-ping dnsutils language-pack-ko ffmpeg openjdk-11-jre-headless libatlas-base-dev libgflags-dev \
    libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libprotobuf-dev libsnappy-dev protobuf-compiler ghostscript python3-tk \
    software-properties-common gpg librdmacm1 libibverbs1 ibverbs-providers openssh-server supervisor \
 && apt-get autoclean && apt-get autoremove
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen \
 && rm -rf /bin/sh \
 && ln -s /bin/bash /bin/sh

# Create a non-root user
ARG USERNAME=rsnet
ARG PASSWORD=rsnet
ARG UID=1000
ARG GID=1000
ENV USER $USERNAME
ENV UID $UID
ENV GID $GID
ENV HOME /home/$USER

RUN groupadd -g $GID $USER \
 && adduser --disabled-password \
    --gecos "Non-root user" \
    --uid $UID \
    --gid $GID \
    --home $HOME \
    $USER \
 && echo $USER:$PASSWORD | chpasswd \
 && adduser $USER sudo \
 && echo $USER 'ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
 && usermod -a -G $USER $USER

USER $USER
WORKDIR $HOME

# Install Miniconda
ARG VERSION_MINICONDA=latest
ARG VERSION_PYTHON=3.9
ENV CONDA_DIR $HOME/miniconda3
ENV PATH=${CONDA_DIR}/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${VERSION_MINICONDA}-Linux-x86_64.sh -O ~/miniconda.sh \
 && chmod +x ~/miniconda.sh \
 && /bin/bash ~/miniconda.sh -b -u -p $CONDA_DIR \
 && rm ~/miniconda.sh \
 && conda install -y libgcc tini python=${VERSION_PYTHON} \
 && conda config --system --prepend channels conda-forge \
 && conda update --all -y \
 && conda init bash \
 && conda clean -afy