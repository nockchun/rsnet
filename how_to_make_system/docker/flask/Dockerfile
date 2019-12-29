# base image
# FROM ubuntu:18.04
FROM ubuntu:latest

# Define Global Main Environments
ENV MINICONDA_VERSION 4.5.11
ENV TZ Asia/Seoul

# Base Environments Setting Up
RUN apt-get update --fix-missing \
 && apt-get install -y --no-install-recommends wget bzip2 ca-certificates curl git locales language-pack-ko dialog apt-utils \
 && echo "ko_KR.UTF-8" > /etc/locale.gen \
 && locale-gen \
 && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
 && echo $TZ > /etc/timezone
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# Install Miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc
ENV PATH /opt/conda/bin:$PATH

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

# load in the environment.yml file
ADD flask/environment.yml /

# create the conda environmnt
RUN conda update -n base conda -y && conda env update

# Copy App into the container
EXPOSE 5000
VOLUME /app

# Run Contained Program
WORKDIR /app
# ENTRYPOINT ["tini", "-g", "--"]