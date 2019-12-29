FROM ubuntu:18.04
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
 && chown -R $NB_USER:$NB_USER $CONDA_DIR \
 && adduser $NB_USER sudo \
 && echo 'rsnet ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER $NB_USER
WORKDIR $HOME

# Install conda
#ENV MINICONDA_VERSION=4.3.21 \
#    CONDA_VERSION=4.7.5 \
ENV MINICONDA_VERSION=latest \
    CONDA_VERSION=4.7.12
RUN mkdir -p .conda

ADD environment.tf2.yml environment.yml
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
 && rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
 && conda config --system --prepend channels conda-forge \
 && conda config --system --set auto_update_conda false \
 && conda config --system --set show_channel_urls true \
 && conda install -y python=3.7 tini=0.18.0 \
 && conda install --quiet --yes conda="${CONDA_VERSION%.*}.*" \
 && conda install -c conda-forge --yes notebook jupyterhub jupyterlab \
 && conda update --all -y

RUN jupyter notebook --generate-config \
 && conda update -n base conda -y \
 && conda env update \
 && rm environment.yml \
 && conda install -c plotly jupyterlab-dash -y

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
    @jupyterlab/fasta-extension @jupyterlab/katex-extension
    # @ryantam626/jupyterlab_code_formatter \
 # && jupyter serverextension enable --py jupyterlab_code_formatter

# Create Tensorflow 1 Environments
# ADD environment.tf.yml environment.yml
# RUN conda env update \
#  && rm environment.yml
# RUN ["/bin/bash" , "-c", "source activate tf2 && \
#     ipython kernel install --user --name tf2 --display-name 'Tensorflow 2' && \
#     conda deactivate"]

# Setting Up JupyterLab Environments
USER root
EXPOSE 8888
EXPOSE 6006
EXPOSE 22
VOLUME /notebooks
VOLUME /tensorboard
RUN chown -R $NB_USER /notebooks \
 && chown -R $NB_USER /tensorboard

# Setting up container startup
ENTRYPOINT ["tini", "-g", "--"]

USER $NB_USER
WORKDIR /notebooks
