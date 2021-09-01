FROM ubuntu:18.04
MAINTAINER RealStudy.NET <nockchun@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

# Install system packages
RUN sed -i 's/archive.ubuntu.com/ftp.harukasan.org/g' /etc/apt/sources.list \
 && apt clean && apt update && apt install -yq --no-install-recommends apt-utils \
      ca-certificates sudo locales fonts-liberation bzip2 gcc g++ make git graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin wget curl npm \
      vim net-tools openssh-server sudo cmake zlib1g-dev libjpeg-dev xvfb xorg-dev xcftools \
      libpng-dev libtiff5 libtiff5-dev xvfb xserver-xephyr vnc4server python-opengl \
 && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH

# Install conda
ENV MINICONDA_VERSION=latest
RUN mkdir -p .conda

# Create MiniConda Environments as Base
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
ADD environment.yml environment.yml
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
    @jupyterlab/shortcuts-extension @jupyterlab/statusbar-extension @jupyterlab/terminal-extension @jupyterlab/tooltip-extension @jupyterlab/ui-components-extension
RUN jupyter labextension install jupyterlab_tensorboard @kiteco/jupyterlab-kite

# Setting Up JupyterLab Environments
EXPOSE 8888
EXPOSE 22
VOLUME /notebooks

ADD notebooks /notebooks

# Setting up container startup
ENTRYPOINT ["tini", "-g", "--"]

WORKDIR /notebooks