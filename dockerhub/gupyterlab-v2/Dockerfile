ARG IMAGE_BASE
FROM ${IMAGE_BASE}
LABEL authors="RealStudy.NET <nockchun@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/conda/bin:$PATH" \
    TF_CPP_MIN_LOG_LEVEL=2 \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH \
    TF_FORCE_GPU_ALLOW_GROWTH=true \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    TZ=Asia/Seoul
# SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install dependencies
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

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
 && bash /tmp/miniconda.sh -b -p /opt/conda \
 && rm /tmp/miniconda.sh \
 && /opt/conda/bin/conda clean -afy

RUN conda update -n base -c defaults conda \
 && conda install -y -n base -c conda-forge python=3.9 jupyterlab numpy=1.26.4 \
    jupyter_bokeh ipykernel ipytest ipympl ipywidgets statsmodels graphviz pyopencl scikit-learn sentencepiece pykalman gplearn \
    pillow firefox geckodriver apscheduler scipy pandas pandas-profiling pandas-datareader jupyterlab-git jupyterlab-latex \
 && conda clean -afy

# Create a Conda environment with JupyterLab, TensorFlow, and PyTorch
RUN conda install -y -n base pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia \
    && conda clean -afy

ARG VERSION_TF
ENV TF_GPU_THREAD_MODE=gpu_shared \
    TF_FORCE_GPU_ALLOW_GROWTH=true
RUN pip install --no-cache-dir numpy==1.26.4 tensorrt nvidia-pyindex nvidia-tensorrt tensorrt-dispatch tensorrt-lean tensorflow==${VERSION_TF} tensorflow-addons streamlit tensorflow-datasets tensorflow-probability
# RUN conda install -y -n base -c conda-forge numpy==1.21.6 protobuf==3.20.* tensorflow-gpu \
#     && conda clean -afy

RUN pip install --no-cache-dir numpy==1.26.4 opencv-python gym gymnasium gymnasium[classic-control] deap gymnasium[atari,accept-rom-license] gymnasium[box2d] gym-notebook-wrapper ray[all] tables nengo[all] lz4 nltk poetry tsaug seasonal pydot einops typing-extensions \
    python-kubernetes pyts dash tortoise-orm html5lib more-itertools httplib2 celery psycopg2 asyncpg tqdm deap asyncio nest-asyncio \
 && pip install --no-cache-dir numpy==1.26.4 danbi ta pandas-ta selenium backtrader yfinance transitions plotly filterpy

#  RUN conda install -y -n base numpy==1.26.4
#  RUN conda install -y -n base numpy==1.24
# 1.23.5
# RUN pip uninstall numpy

# Expose JupyterLab default port
EXPOSE 8888

# Set the default command to start JupyterLab
# CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]