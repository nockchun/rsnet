FROM nvidia/cuda:11.4.1-devel-ubuntu20.04
LABEL maintainer="Jaehong. Kim. <nockchun@gmail.com>"

# Setup OS Base System Packages
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

SHELL ["/bin/bash", "--login", "-c"]
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt update --fix-missing && apt clean && apt update \
 && apt install -y --no-install-recommends apt wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
        sudo locales fonts-liberation vim net-tools openssh-client graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin \
        autoconf automake dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake \
        libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev \
        libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb \
        libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
        iputils-ping dnsutils language-pack-ko python-opengl ffmpeg openjdk-11-jre-headless libatlas-base-dev libgflags-dev \
        libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libprotobuf-dev libsnappy-dev protobuf-compiler ghostscript python3-tk \
 && echo "ko_KR.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen

# Install Fonts
RUN apt install unzip fonts-unfonts-core fonts-unfonts-extra fonts-baekmuk fonts-nanum fonts-nanum-coding fonts-nanum-extra fonts-ubuntu-font-family-console \
 && wget https://github.com/naver/d2codingfont/releases/download/VER1.21/D2Coding-1.2.zip \
 && mkdir /usr/share/fonts/truetype/D2Coding \
 && unzip D2Coding-1.2.zip -d /usr/share/fonts/truetype/D2Coding/ \
 && rm -rf /usr/share/fonts/truetype/D2Coding/__MACOSX \
 && rm -rf D2Coding-1.2.zip \
 && wget -O mac-fonts.zip http://drive.noobslab.com/data/Mac/macfonts.zip \
 && unzip mac-fonts.zip -d /usr/share/fonts \
 && rm mac-fonts.zip \
 && fc-cache -f -v

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    LC_ALL=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH

# Create MiniConda Environments as Base
ENV MINICONDA_VERSION=latest
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
 && rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && conda config --system --prepend channels conda-forge \
 && conda config --system --set show_channel_urls true \
 && conda install -y tini=0.18.0 \
 && conda update -n base -c defaults conda \
 && conda update --all -y \
 && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
 && conda install -c conda-forge --yes notebook jupyterhub jupyterlab \
 && jupyter notebook --generate-config

# Create Tensorflow 2 Environments
ADD conda-forge.yml environment.yml
RUN conda update -y pip setuptools \
 && python -m pip install --upgrade pip setuptools \
 && conda env update --name base --file environment.yml \
 && rm environment.yml

# Adding Jupyterlab Extensions
RUN jupyter serverextension enable --py jupyterlab --sys-prefix \
 && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
    @jupyterlab/application-extension @jupyterlab/apputils-extension @jupyterlab/codemirror-extension @jupyterlab/completer-extension \
    @jupyterlab/console-extension @jupyterlab/csvviewer-extension @jupyterlab/docmanager-extension @jupyterlab/documentsearch-extension \
    @jupyterlab/extensionmanager-extension @jupyterlab/filebrowser-extension @jupyterlab/fileeditor-extension @jupyterlab/help-extension \
    @jupyterlab/htmlviewer-extension @jupyterlab/hub-extension @jupyterlab/imageviewer-extension @jupyterlab/inspector-extension \
    @jupyterlab/javascript-extension @jupyterlab/json-extension @jupyterlab/launcher-extension @jupyterlab/logconsole-extension \
    @jupyterlab/mainmenu-extension @jupyterlab/markdownviewer-extension @jupyterlab/mathjax2-extension @jupyterlab/notebook-extension \
    @jupyterlab/pdf-extension @jupyterlab/rendermime-extension @jupyterlab/running-extension @jupyterlab/settingeditor-extension \
    @jupyterlab/shortcuts-extension @jupyterlab/statusbar-extension @jupyterlab/terminal-extension \
    @jupyterlab/theme-dark-extension @jupyterlab/theme-light-extension @jupyterlab/tooltip-extension @jupyterlab/ui-components-extension \
    @jupyterlab/vdom-extension @jupyterlab/vega5-extension @jupyterlab/git @krassowski/jupyterlab-lsp
RUN jupyter labextension install @kiteco/jupyterlab-kite

# Setting up container startup
EXPOSE 8888
EXPOSE 6006
EXPOSE 8265

VOLUME /notebooks
VOLUME /ml_data
VOLUME /tensorboard

# Setting up container startup
ENTRYPOINT ["tini", "-g", "--"]

WORKDIR /notebooks
