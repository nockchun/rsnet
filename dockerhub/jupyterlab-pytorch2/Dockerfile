ARG IMAGE_BASE
FROM ${IMAGE_BASE}
LABEL authors="RealStudy.NET <nockchun@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/conda/bin:$PATH" \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    TZ=Asia/Seoul

# Install dependencies
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt-get update --fix-missing \
 && apt-get upgrade -y \
 && apt-get install -yq --no-install-recommends \
    debconf apt wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
    tzdata fonts-liberation fonts-nanum* net-tools vim openssh-client graphviz libgraphviz-dev libhdf5-dev openmpi-bin pandoc run-one \
    autoconf automake dpkg-dev file build-essential g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake ninja-build \
    libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev htop cm-super dvipng \
    libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb less libtcmalloc-minimal4 \
    libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
    iputils-ping dnsutils language-pack-ko ffmpeg openjdk-17-jre-headless libatlas-base-dev libgflags-dev inkscape texlive texlive-xetex texlive-fonts-recommended texlive-plain-generic \
    texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science tipa \
    libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libprotobuf-dev libsnappy-dev protobuf-compiler ghostscript python3-tk python3-dev \
    software-properties-common gpg librdmacm1 libibverbs1 ibverbs-providers openssh-server supervisor tini \
    sox libcairo2-dev libpango1.0-dev libboost-all-dev swig libarchive-dev zsh libnuma-dev wkhtmltopdf \
 && apt autoremove -y \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
 && bash /tmp/miniconda.sh -b -p /opt/conda \
 && rm /tmp/miniconda.sh \
 && /opt/conda/bin/conda clean -afy

# Install basic library (추천: VERSION_PYTHON=3.11, VERSION_NUMPY=2.1)
ARG VERSION_PYTHON=3.11
ARG VERSION_NUMPY=2.1
RUN conda init bash \
 && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main \
 && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r \
 && conda update -n base -c defaults -y conda \
 && conda config --add channels conda-forge \
 && conda config --set channel_priority strict \
 && conda install -y -n base -c conda-forge \
        python==${VERSION_PYTHON} \
        numpy==${VERSION_NUMPY} \
        scipy \
        pandas \
 && conda clean -afy

# Setup JupyterLab plugins (JupyterLab 4.4 최신 유지)
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main \
 && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r \
 && conda install -c conda-forge -y \
        starship \
        nodejs=20.* \
        pandoc \
        texlive-core \
        texlab \
        chktex \
 && pip install --no-cache-dir \
    'jupyterlab==4.4.10' \
    'jupyterlab-lsp==5.2.0' \
    'python-lsp-server[all]==1.13.1' \
    'jupyterlab-code-formatter==3.0.2' \
    black \
    isort \
    'jupyterlab-latex==4.3.0' \
    'jupyter-resource-usage==1.0.0' \
    'jupyterlab-git==0.51.2' \
    'ipywidgets>=8.0' \
    'jupyter_bokeh' \
    'jupyterlab-execute-time==3.2.0' \
 && npm set prefix /root \
 && npm install -g --save-dev \
    remark-language-server \
    remark-preset-lint-consistent \
    remark-preset-lint-recommended \
 && mkdir -p /usr/local/etc/jupyter \
 && jupyter labextension disable --level=system "@jupyterlab/apputils-extension:announcements" \
 && conda clean -a -y && pip cache purge && npm cache clean --force

# (옵션) 깜박임 유발 가능 확장
# RUN pip install --no-cache-dir 'jupyterlab-spellchecker==0.8.4' 'lckr_jupyterlab_variableinspector==3.2.4' 'jupyterlab_wakatime==0.2.0'

# 파이썬 빌드 의존성
RUN pip install --no-cache-dir -U \
    pip \
    wheel \
    setuptools \
    setuptools-scm \
    packaging \
    cmake \
    ninja \
    pybind11 \
    scikit-build-core

# --------------------------------------------------------------------
# PyTorch 2.8.0 + CUDA 12.8 + Triton 3.4.0 (vLLM / Unsloth 조합에서 검증됨)
# --------------------------------------------------------------------
RUN pip install --no-cache-dir \
    "torch==2.8.0" \
    "torchvision==0.23.0" \
    "torchaudio==2.8.0" \
    --index-url https://download.pytorch.org/whl/cu128

# Triton 커널 (PyTorch 2.8.0 권장 버전)
RUN pip install --no-cache-dir \
    "triton==3.4.0" \
    --index-url https://download.pytorch.org/whl

# --------------------------------------------------------------------
# Additional base libraries
# --------------------------------------------------------------------
RUN pip install --no-cache-dir \
    graphviz \
    pyopencl \
    sentencepiece \
    pillow \
    geckodriver \
    apscheduler \
    statsmodels \
    scikit-learn \
    ipykernel \
    ipytest \
    ipympl \
    pykalman \
    gplearn \
    opencv-python \
    gym \
    gymnasium \
    "gymnasium[classic-control]" \
    deap \
    evaluate \
    pygad \
    "gymnasium[atari,accept-rom-license]" \
    "gymnasium[box2d]" \
    gym-notebook-wrapper \
    "ray[all]" \
    tables \
    "nengo[all]" \
    lz4 \
    nltk \
    poetry \
    tsaug \
    seasonal \
    pydot \
    einops \
    typing-extensions \
    python-kubernetes \
    pyts \
    dash \
    tortoise-orm \
    html5lib \
    more-itertools \
    httplib2 \
    celery \
    psycopg2 \
    asyncpg \
    tqdm \
    asyncio \
    nest-asyncio \
    werkzeug \
    torchinfo \
    torchview \
 && pip install --no-cache-dir \
    danbi \
    ta \
    selenium \
    backtrader \
    yfinance \
    transitions \
    plotly \
    filterpy \
    orjson \
    nats-py \
    dbutils \
    pandas-profiling \
    pandas-datareader \
    protobuf \
 && pip install --no-cache-dir \
    wandb \
    openai \
    langchain_community \
    langchain-huggingface \
    huggingface_hub \
    chromadb \
    pymilvus \
    opensearch-py \
    pymupdf \
    pdfminer.six \
    pdfplumber \
    pymupdf4llm \
    pdfkit \
    pypdf \
    markdownify \
    safetensors

# --------------------------------------------------------------------
# Unsloth & LLM fine-tuning 스택 (torch 2.8 + vLLM 0.11 + Transformers 4.57.1 기준)
# --------------------------------------------------------------------
# Unsloth만 --no-deps 로 설치해서 torch 버전을 건드리지 않게 함
RUN pip install --no-cache-dir --no-deps \
    unsloth \
    unsloth_zoo \
 && pip install --no-cache-dir \
    "transformers==4.57.1" \
    "xformers==0.0.32.post1" \
    bitsandbytes \
    "trl==0.24.0" \
    accelerate \
    peft \
    hf_transfer

RUN pip install --no-cache-dir \
    sentence-transformers \
    auto_gptq \
    autoawq \
    autotrain-advanced \
    gradio \
    streamlit \
    datasets \
    timm \
    docling docling-core \
    langchain \
    langchain-core \
    langchain-text-splitters \
    langchain-openai \
    langchain-milvus \
    langchain-docling \
    langchain-qdrant \
    langchain-chroma \
    langchain-ollama \
    langchain-experimental \
    bs4 \
    langgraph \
    wikipedia

# --------------------------------------------------------------------
# vLLM (0.11.0 태그 사용, torch 2.8 + CUDA 12.8 환경에서 검증)
# --------------------------------------------------------------------
RUN git clone --recursive https://github.com/vllm-project/vllm /tmp/vllm \
 && cd /tmp/vllm \
 && git fetch --tags \
 && git checkout v0.11.0 \
 && CUDA_HOME=/usr/local/cuda pip install --no-build-isolation --no-deps . \
 && cd / \
 && rm -rf /tmp/vllm

# --------------------------------------------------------------------
# llama.cpp (HF → GGUF 변환 의존성만 venv에 격리 설치)
# --------------------------------------------------------------------
ENV LLAMA_CPP_DIR=/opt/llama.cpp \
    LLAMA_CPP_VENV=/opt/llama.cpp/.venv

RUN git clone --depth=1 https://github.com/ggml-org/llama.cpp ${LLAMA_CPP_DIR} \
 && python -m venv ${LLAMA_CPP_VENV} \
 && ${LLAMA_CPP_VENV}/bin/python -m pip install --upgrade pip \
 && ${LLAMA_CPP_VENV}/bin/pip install --no-cache-dir -r ${LLAMA_CPP_DIR}/requirements/requirements-convert_hf_to_gguf.txt \
 && printf '%s\n' '#!/usr/bin/env bash' \
      'set -euo pipefail' \
      'LLAMA_DIR="${LLAMA_CPP_DIR:-/opt/llama.cpp}"' \
      'VENV="${LLAMA_CPP_VENV:-$LLAMA_DIR/.venv}"' \
      'if   [ -f "$LLAMA_DIR/convert_hf_to_gguf.py" ]; then SCRIPT="$LLAMA_DIR/convert_hf_to_gguf.py";' \
      'elif [ -f "$LLAMA_DIR/convert-hf-to-gguf.py" ]; then SCRIPT="$LLAMA_DIR/convert-hf-to-gguf.py";' \
      'elif [ -f "$LLAMA_DIR/convert.py" ]; then SCRIPT="$LLAMA_DIR/convert.py";' \
      'else echo "No converter script found in $LLAMA_DIR" >&2; exit 1; fi' \
      'exec "$VENV/bin/python" "$SCRIPT" "$@"' \
    > /usr/local/bin/convert-hf-to-gguf \
 && chmod +x /usr/local/bin/convert-hf-to-gguf

# Setup oh-my-zsh
RUN git clone https://github.com/ohmyzsh/ohmyzsh.git /root/.oh-my-zsh \
 && cp /root/.oh-my-zsh/templates/zshrc.zsh-template /root/.zshrc \
 && sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/g' /root/.zshrc
ENV SHELL=/usr/bin/zsh

# /notebook 생성 및 Git safe.directory 등록
RUN mkdir -p /notebook \
 && git config --system --add safe.directory /notebook \
 && git config --global --add safe.directory /notebook

# 데이터 볼륨 선언
VOLUME ["/notebook"]

ENTRYPOINT ["/usr/bin/zsh", "-c", "exec \"$@\"", "--"]
