FROM nvidia/cuda:10.2-cudnn7-base-ubuntu18.04
LABEL maintainer="Jaehong. Kim. <nockchun@gmail.com>"

# Setup OS Base System Packages
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt update --fix-missing && apt clean && apt update \
 && apt install -y --no-install-recommends wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
        sudo locales fonts-liberation vim net-tools openssh-client graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin \
        autoconf automake dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake \
        libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev \
        libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb \
        libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
        iputils-ping dnsutils language-pack-ko python-opengl ffmpeg \
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

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash rsnet \
 && chown -R rsnet:rsnet /app
RUN echo "rsnet ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-rsnet
USER rsnet

# All users can use /home/user as their home directory
ENV HOME=/home/rsnet
RUN chmod 777 /home/rsnet

# Configure Environments
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    LC_ALL=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8 \
    PATH=$CONDA_DIR/bin:$HOME/.local/bin:$PATH \
    HOME=/home/rsnet

# Create MiniConda Environments as Base
ENV MINICONDA_VERSION=latest
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
 && rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && conda install -y python==3.8.1 \
 && sudo ln -s /opt/conda/bin/conda /usr/bin/conda \
 && sudo ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
 && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
 && echo "conda activate base" >> ~/.bashrc \
 && conda update -y pip setuptools \
 && python -m pip install --upgrade pip setuptools \
 && pip install ez_setup \
 && conda clean -ya

# Install Basic Conda Library
ADD conda-forge.yml environment.yml
RUN chown -R $NB_USER.$NB_USER $CONDA_DIR \
 && conda env update --name base --file environment.yml \
 && rm environment.yml \
 && jupyter notebook --generate-config

# CUDA 10.2-specific pytorch steps
RUN conda install -y -c pytorch \
    cudatoolkit=10.2 \
    "pytorch=1.5.1=py3.8_cuda10.2.89_cudnn7.6.5_0" \
    "torchvision=0.6.1=py38_cu102" \
 && conda clean -ya

# Adding Jupyterlab Extensions
RUN jupyter serverextension enable --py jupyterlab --sys-prefix \
 && jupyter labextension install @jupyter-widgets/jupyterlab-manager@2 \
    @jupyterlab/application-extension @jupyterlab/apputils-extension @jupyterlab/codemirror-extension @jupyterlab/completer-extension \
    @jupyterlab/console-extension @jupyterlab/csvviewer-extension @jupyterlab/docmanager-extension @jupyterlab/documentsearch-extension \
    @jupyterlab/extensionmanager-extension @jupyterlab/filebrowser-extension @jupyterlab/fileeditor-extension @jupyterlab/help-extension \
    @jupyterlab/htmlviewer-extension @jupyterlab/hub-extension @jupyterlab/imageviewer-extension @jupyterlab/inspector-extension \
    @jupyterlab/javascript-extension @jupyterlab/json-extension @jupyterlab/launcher-extension @jupyterlab/logconsole-extension \
    @jupyterlab/mainmenu-extension @jupyterlab/markdownviewer-extension @jupyterlab/mathjax2-extension @jupyterlab/notebook-extension \
    @jupyterlab/pdf-extension @jupyterlab/rendermime-extension @jupyterlab/running-extension @jupyterlab/settingeditor-extension \
    @jupyterlab/shortcuts-extension @jupyterlab/statusbar-extension @jupyterlab/tabmanager-extension @jupyterlab/terminal-extension \
    @jupyterlab/theme-dark-extension @jupyterlab/theme-light-extension @jupyterlab/tooltip-extension @jupyterlab/ui-components-extension \
    @jupyterlab/vdom-extension @jupyterlab/vega5-extension
RUN jupyter labextension install jupyter-matplotlib @jupyterlab/fasta-extension @jupyterlab/toc @jupyterlab/mathjax3-extension \
    @jupyterlab/geojson-extension @jupyterlab/katex-extension @lckr/jupyterlab_variableinspector

# Setting Up JupyterLab Environments
EXPOSE 8888
EXPOSE 6006
EXPOSE 22
VOLUME /notebooks
VOLUME /ml_data
VOLUME /tensorboard
RUN sudo chown -R $NB_USER.$NB_USER /notebooks

# Setting up container startup
ENTRYPOINT ["tini", "-g", "--"]

WORKDIR /notebooks
