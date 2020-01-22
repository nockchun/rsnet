FROM nvidia/cuda:10.1-base-ubuntu18.04
LABEL maintainer="Jaehong. Kim. <nockchun@gmail.com>"

ARG NB_USER="rsnet"
ARG NB_UID="1000"
ENV DEBIAN_FRONTEND noninteractive

# Install system packages
RUN sed -i 's/archive.ubuntu.com/ftp.harukasan.org/g' /etc/apt/sources.list \
 && apt clean && apt update && apt install -yq --no-install-recommends apt-utils \
    ca-certificates sudo locales fonts-liberation bzip2 gcc g++ make git graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin wget curl npm \
    vim net-tools openssh-server sudo cmake zlib1g-dev libjpeg-dev xvfb xorg-dev xcftools \
    libpng-dev libtiff5 libtiff5-dev xvfb xserver-xephyr vnc4server python-opengl \
 && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen

# Install Fonts
RUN apt install unzip fonts-unfonts-core fonts-unfonts-extra fonts-baekmuk fonts-nanum fonts-nanum-coding fonts-nanum-extra \
 && wget https://github.com/naver/d2codingfont/releases/download/VER1.21/D2Coding-1.2.zip \
 && mkdir /usr/share/fonts/truetype/D2Coding \
 && unzip D2Coding-1.2.zip -d /usr/share/fonts/truetype/D2Coding/ \
 && rm -rf /usr/share/fonts/truetype/D2Coding/__MACOSX \
 && fc-cache -f -v

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
RUN groupadd -g $NB_UID $NB_USER \
 && useradd -m -s /bin/bash -p $NB_USER -g $NB_USER -N -u $NB_UID $NB_USER \
 && mkdir -p $CONDA_DIR \
 && chown -R $NB_USER.$NB_USER $CONDA_DIR \
 && adduser $NB_USER sudo \
 && echo 'rsnet ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER $NB_USER
WORKDIR $HOME

# Install conda
ENV MINICONDA_VERSION=latest \
    CONDA_VERSION=4.7.12
RUN mkdir -p .conda

# Create Tensorflow 2 Environments as Base
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
 && rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && conda config --system --prepend channels conda-forge \
 && conda config --system --set auto_update_conda true \
 && conda config --system --set show_channel_urls true \
 && conda install -y tini=0.18.0 \
 && conda update -n base -c defaults conda \
 && conda update --all -y \
 && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
 && conda install -c conda-forge --yes notebook jupyterhub jupyterlab \
 && jupyter notebook --generate-config \
 && conda install -c plotly jupyterlab-dash -y

ADD environment.tf2.yml environment.yml
RUN conda update -y pip setuptools \
 && python -m pip install --upgrade pip setuptools \
 && conda env update --name base --file environment.yml \
 && rm environment.yml

RUN jupyter serverextension enable --py jupyterlab --sys-prefix \
 && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
    jupyter-threejs jupyter-matplotlib \
    @jupyterlab/vega3-extension @jupyterlab/vega4-extension @jupyterlab/vega5-extension \
    ipysheet ipyvolume jupyterlab-dash jupyterlab-drawio \
    @jupyterlab/toc @krassowski/jupyterlab_go_to_definition \
    @jupyterlab/notebook-extension @jupyterlab/terminal-extension \
    @jupyterlab/plotly-extension @jupyterlab/json-extension \
    @jupyterlab/imageviewer-extension @jupyterlab/geojson-extension \
    @jupyterlab/tooltip-extension @jupyterlab/help-extension @jupyterlab/running-extension \
    @jupyterlab/inspector-extension @jupyterlab/pdf-extension @jupyterlab/mathjax2-extension \
    @jupyterlab/vdom-extension @jupyterlab/hub-extension @jupyterlab/latex \
    @jupyterlab/fasta-extension @jupyterlab/katex-extension \
    @ryantam626/jupyterlab_code_formatter \
 && jupyter serverextension enable --py jupyterlab_code_formatter

# Create Tensorflow 1 Environments
ADD environment.yml environment.yml
RUN conda env update --name tf1 --file environment.yml \
 && rm environment.yml
RUN ["/bin/bash" , "-c", "source activate tf1 && \
    ipython kernel install --user --name tf1 --display-name 'Tensorflow 1' && \
    conda deactivate"]

# Setting Up JupyterLab Environments
USER root
EXPOSE 8888
EXPOSE 6006
EXPOSE 22
VOLUME /notebooks
VOLUME /notebooks/ml_data
VOLUME /notebooks/tensorboard
RUN chown -R $NB_USER /notebooks

# Setting up container startup
ENTRYPOINT ["tini", "-g", "--"]

USER $NB_USER
WORKDIR /notebooks