ARG IMAGE_BASE
FROM ${IMAGE_BASE}
LABEL authors="RealStudy.NET <nockchun@gmail.com>"

# install apt-utils in header to fix warnings in docker-stacks
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y install apt-utils sudo locales
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install system packages
ENV LC_ALL=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt-get update --fix-missing \
 && apt-get upgrade -y \
 && apt-get install -yq --no-install-recommends debconf apt wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
    tzdata fonts-liberation vim net-tools openssh-client graphviz libgraphviz-dev libgl1-mesa-glx libhdf5-dev openmpi-bin pandoc run-one \
    autoconf automake dpkg-dev file build-essential g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake \
    libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev htop cm-super dvipng \
    libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb less \
    libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
    iputils-ping dnsutils language-pack-ko ffmpeg openjdk-17-jre-headless libatlas-base-dev libgflags-dev inkscape texlive-xetex texlive-fonts-recommended texlive-plain-generic \
    libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libprotobuf-dev libsnappy-dev protobuf-compiler ghostscript python3-tk \
    software-properties-common gpg librdmacm1 libibverbs1 ibverbs-providers openssh-server supervisor libcudnn8-dev tensorrt tini \
 && apt-get autoclean && apt-get autoremove
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen \
 && rm -rf /bin/sh \
 && ln -s /bin/bash /bin/sh \
 && rm -rf /var/lib/apt/lists/*

# 사용자 'myuser'를 생성합니다.
ARG USERNAME=user
ENV USER=${USERNAME}
ENV HOME /home/$USER
RUN useradd -m ${USER} \
 && echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $USERNAME
WORKDIR $HOME

# Install Miniconda
ARG VERSION_MINICONDA=latest
ARG VERSION_PYTHON=3.10
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

ENTRYPOINT ["tini", "-g", "--"]

# Install jupyterlab ###########################################################################################
RUN conda install -c conda-forge --yes notebook jupyterhub jupyterlab \
 && jupyter notebook --generate-config \
 && jupyter lab clean

RUN pip install --no-cache-dir --upgrade \
    jupyter-server jupyter_contrib_nbextensions jupyter_nbextensions_configurator \
    jupyterlab-git plotly jupyterlab-drawio rise \
    ipyleaflet ipywidgets jupyterlab-spellchecker
RUN conda install -c conda-forge jupyter_bokeh jupyterlab-lsp jupyter-lsp-python jupyterlab-dash ipykernel ipytest ipympl
RUN pip install jupyter_scheduler \
 && jupyter lab --generate-config

# Install tensorflow ###########################################################################################
ARG VERSION_TF
RUN pip install tensorrt nvidia-pyindex nvidia-tensorrt tensorrt-dispatch tensorrt-lean tensorflow==${VERSION_TF} tensorflow-addons streamlit tensorflow-datasets

# Install pytorch ##############################################################################################
# RUN conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install library ##############################################################################################
RUN conda install -c anaconda redis openpyxl statsmodels
RUN conda install -c conda-forge scikit-learn sentencepiece pykalman gplearn
RUN pip install opencv-python gym ray[all] tables nengo[all] lz4 nltk poetry tsaug seasonal pydot einops pandas-profiling pandas-datareader typing-extensions \
    python-kubernetes pyts dash tortoise-orm html5lib more-itertools httplib2 celery psycopg2 asyncpg
RUN pip install danbi ta pandas-ta

EXPOSE 8888
VOLUME /notebook
WORKDIR /notebook
