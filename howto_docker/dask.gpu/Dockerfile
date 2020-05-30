FROM nvidia/cuda:10.1-base-ubuntu18.04
LABEL maintainer="Jaehong. Kim. <nockchun@gmail.com>"

ARG NB_USER="asa"
ARG NB_UID="1000"
ENV DEBIAN_FRONTEND noninteractive

# Install system packages
RUN apt update && apt install -yq --no-install-recommends \
      ca-certificates sudo locales fonts-liberation bzip2 gcc g++ make git graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin wget curl npm \
 && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen \
 && rm -rf /var/lib/apt/lists/*

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    HOME=/home/$NB_USER

# Create jovyan user with UID=1000 and in the 'users' group 
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER \
 && mkdir -p $CONDA_DIR \
 && chown -R $NB_USER $CONDA_DIR

USER $NB_USER
WORKDIR $HOME

# Install conda
#ENV MINICONDA_VERSION=4.3.21 \
#    CONDA_VERSION=4.7.5 \
ENV MINICONDA_VERSION=latest \
    CONDA_VERSION=4.7.11 \
    CONDA_DIR=/opt/conda \
    PATH=$CONDA_DIR/bin:$PATH

# Create Tensorflow 2 Environments
ADD environment.tf2.yml environment.yml
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
 && rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && conda config --system --prepend channels conda-forge \
 && conda config --system --set auto_update_conda false \
 && conda config --system --set show_channel_urls true \
 && conda install -y python=3.7 tini=0.18.0 \
 && conda upgrade --all --yes \
 && conda install --quiet --yes conda="${CONDA_VERSION%.*}.*" \
 && conda env update \
 && rm environment.yml

USER $NB_USER
# Setting up container startup
ENTRYPOINT ["tini", "-g", "--"]
