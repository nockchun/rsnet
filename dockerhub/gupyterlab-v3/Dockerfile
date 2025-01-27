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
    tzdata fonts-liberation fonts-nanum* vim net-tools openssh-client graphviz libgraphviz-dev libgl1-mesa-glx libhdf5-dev openmpi-bin pandoc run-one \
    autoconf automake dpkg-dev file build-essential g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake \
    libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev htop cm-super dvipng \
    libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb less libtcmalloc-minimal4 \
    libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
    iputils-ping dnsutils language-pack-ko ffmpeg openjdk-17-jre-headless libatlas-base-dev libgflags-dev inkscape texlive texlive-xetex texlive-fonts-recommended texlive-plain-generic \
    texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science tipa \
    libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libprotobuf-dev libsnappy-dev protobuf-compiler ghostscript python3-tk python3-dev \
    software-properties-common gpg librdmacm1 libibverbs1 ibverbs-providers openssh-server supervisor libcudnn8-dev tensorrt tini \
    sox libcairo2-dev libpango1.0-dev libboost-all-dev swig libarchive-dev \
 && apt autoremove \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

# RUN LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 \
#  && echo "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" >> /etc/profile

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen \
 && rm -rf /bin/sh \
 && ln -s /bin/bash /bin/sh

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
 && conda install -y libgcc python=${VERSION_PYTHON} \
 && conda config --system --prepend channels conda-forge \
 && conda update --all -y \
 && conda init bash \
 && conda clean -afy

# Install jupyterlab ###########################################################################################
RUN conda install -c conda-forge --yes \
    notebook jupyterhub jupyterlab jupyter_bokeh ipykernel ipytest ipympl ipywidgets \
    statsmodels graphviz pyopencl scikit-learn sentencepiece pykalman gplearn \
    pillow firefox geckodriver apscheduler scipy numpy>=2 pandas pandas-profiling pandas-datareader jupyterlab-git jupyterlab-latex \
 && jupyter lab --generate-config \
 && jupyter lab build

# Install tensorflow ###########################################################################################
ARG VERSION_TF
RUN pip install --no-cache-dir tensorrt nvidia-pyindex nvidia-tensorrt tensorrt-dispatch tensorrt-lean tensorflow==${VERSION_TF} tensorflow-addons streamlit tensorflow-datasets tensorflow-probability

# Install pytorch ##############################################################################################
ARG PYTORCH
RUN if [ "$PYTORCH" = "true" ]; then \
        conda install pytorch torchvision torchaudio -c pytorch -c nvidia -y; \
    fi

# Install library ##############################################################################################
RUN pip install --no-cache-dir opencv-python gym gymnasium gymnasium[classic-control] deap gymnasium[atari,accept-rom-license] gymnasium[box2d] gym-notebook-wrapper ray[all] tables nengo[all] lz4 nltk poetry tsaug seasonal pydot einops typing-extensions \
    python-kubernetes pyts dash tortoise-orm html5lib more-itertools httplib2 celery psycopg2 asyncpg tqdm deap asyncio nest-asyncio \
 && pip install --no-cache-dir danbi ta pandas-ta selenium jupyterlab-system-monitor backtrader yfinance transitions plotly

# RUN pip install --no-cache-dir --upgrade jupyterlab jupyterlab-git jupyterlab-latex transformers peft trl bitsandbytes accelerate \
#  && jupyter lab --generate-config \
#  && jupyter lab build

 RUN conda install --yes \
 filterpy matplotlib pygraphviz redis openpyxl orjson nats-py numpy>=2

# matplotlib에 Nanum 폰트 추가
RUN cp /usr/share/fonts/truetype/nanum/Nanum* $HOME/miniconda3/lib/python${VERSION_PYTHON}/site-packages/matplotlib/mpl-data/fonts/ttf/ \
 && fc-cache -fv \
 && rm -rf ~/.cache/matplotlib/*

RUN conda clean -afy \
 && sudo rm -rf /root/.cache/pip

EXPOSE 8888
VOLUME /notebook
WORKDIR /notebook
