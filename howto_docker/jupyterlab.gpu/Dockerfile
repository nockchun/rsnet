FROM nvidia/cuda:11.4.0-runtime-ubuntu20.04
LABEL maintainer="Jaehong. Kim. <nockchun@gmail.com>"

# Setup OS Base System Packages
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

SHELL ["/bin/bash", "--login", "-c"]
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt update --fix-missing && apt clean && apt update \
 && apt install -y --no-install-recommends wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
        sudo locales fonts-liberation vim net-tools openssh-client graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin \
        autoconf automake dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake \
        libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev \
        libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb \
        libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
        iputils-ping dnsutils language-pack-ko python-opengl ffmpeg openjdk-11-jre-headless libatlas-base-dev libgflags-dev \
        libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libprotobuf-dev libsnappy-dev protobuf-compiler \
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

# Configure Environments
ARG NB_USER="rsnet"
ARG NB_UID="1000"
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    LC_ALL=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8
ENV PATH=$CONDA_DIR/bin:$HOME/.local/bin:$PATH \
    HOME=/home/$NB_USER

RUN groupadd -g $NB_UID $NB_USER \
 && useradd -m -s /bin/bash -p $NB_USER -g $NB_USER -N -u $NB_UID $NB_USER \
 && mkdir -p $CONDA_DIR \
 && chown -R $NB_USER.$NB_USER $CONDA_DIR \
 && adduser $NB_USER sudo \
 && echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$NB_USER \
 && chmod 0440 /etc/sudoers.d/$NB_USER

# Change User
USER $NB_USER
WORKDIR $HOME

# Create MiniConda Environments as Base
ENV MINICONDA_VERSION=latest
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
 && rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && sudo ln -s /opt/conda/bin/conda /usr/bin/conda \
 && sudo ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
 && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
 && echo "conda activate base" >> ~/.bashrc \
 && conda install --yes nomkl conda-build \
 && conda update --yes pip setuptools \
 && python -m pip install --upgrade pip setuptools \
 && pip install ez_setup

# Install Basic Conda Library
ADD conda-forge.yml environment.yml
RUN chown -R $NB_USER.$NB_USER $CONDA_DIR \
 && conda env update --name base --file environment.yml \
 && rm environment.yml \
 && jupyter lab --generate-config

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
    @jupyterlab/vdom-extension @jupyterlab/vega5-extension @jupyterlab/git
RUN jupyter labextension install jupyter-matplotlib @jupyterlab/fasta-extension @jupyterlab/toc @jupyterlab/mathjax3-extension \
    @jupyterlab/geojson-extension @jupyterlab/katex-extension
#   \
#      @lckr/jupyterlab_variableinspector

# Create PyTorch Environments
ADD pytorch.yml environment.yml
RUN conda create -y -n pytorch ipykernel python=3.8 && conda activate pytorch \
 && conda config --add channels conda-forge \
 && conda install --yes pytorch torchvision torchaudio cudatoolkit=11.0 -c pytorch \
 && ipython kernel install --user --name pytorch --display-name 'PyTorch' \
 && conda env update --name pytorch --file ~/environment.yml \
 && conda deactivate \
 && rm ~/environment.yml

# Tini: https://github.com/krallin/tini
USER root
RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

# Spark Livy Setting
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension \
 && cd /opt/conda/lib/python3.8/site-packages \
 && jupyter-kernelspec install sparkmagic/kernels/sparkkernel --user \
 && jupyter-kernelspec install sparkmagic/kernels/pysparkkernel --user \
 && jupyter-kernelspec install sparkmagic/kernels/sparkrkernel --user 
ADD config.json $HOME/.sparkmagic/config.json

# Setting up container startup
EXPOSE 8888
EXPOSE 6006

VOLUME /notebooks
VOLUME /ml_data
VOLUME /tensorboard

# Cleanning System.
RUN conda clean -aftipy \
 && conda build purge-all \
 && find /opt/conda/ -follow -type f -name '*.a' -delete \
 && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
 && find /opt/conda/ -follow -type f -name '*.js.map' -delete

RUN chown -R $NB_USER.$NB_USER $HOME \
 && chown -R $NB_USER.$NB_USER $CONDA_DIR \
 && chown -R $NB_USER.$NB_USER /notebooks \
 && chown -R $NB_USER.$NB_USER /ml_data \
 && chown -R $NB_USER.$NB_USER /tensorboard

# Setting up container startup
USER $NB_USER
ENTRYPOINT ["tini", "-g", "--"]

WORKDIR /notebooks
