# syntax=docker/dockerfile:1.7

# 원하는 Unsloth 태그로 고정하고 싶으면 빌드 시 BASE_IMAGE를 바꾸세요.
# 예: unsloth/unsloth:2025.11.2-pt2.8.0-cu12.8-trans4.57.0  (Docker Hub / GHCR에 존재)
ARG BASE_IMAGE=unsloth/unsloth:latest
FROM ${BASE_IMAGE}

# Unsloth 컨테이너는 기본적으로 non-root(unsloth) 유저로 실행됩니다. :contentReference[oaicite:1]{index=1}
# 이미지 빌드 단계에서 패키지 설치를 위해 root로 전환합니다.
USER root

# (선택) 시스템 의존성 설치: 필요 없으면 이 블록 제거하세요.
# - build-essential: 일부 pip 패키지 빌드에 필요
# - git/curl: 소스 설치/다운로드용
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
      git curl ca-certificates build-essential \
    && apt-get install -yq --no-install-recommends debconf apt wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
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
    && apt autoremove \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    graphviz pyopencl sentencepiece pillow geckodriver apscheduler statsmodels scikit-learn ipykernel ipytest ipympl pykalman gplearn \
    opencv-python gym gymnasium gymnasium[classic-control] deap evaluate pygad gymnasium[atari,accept-rom-license] gymnasium[box2d] gym-notebook-wrapper ray[all] tables nengo[all] lz4 nltk poetry tsaug seasonal pydot einops typing-extensions \
    python-kubernetes pyts dash tortoise-orm html5lib more-itertools httplib2 celery psycopg2 asyncpg tqdm asyncio nest-asyncio werkzeug torchinfo torchview \
 && pip install --no-cache-dir danbi ta selenium backtrader yfinance transitions plotly filterpy orjson nats-py dbutils pandas-profiling pandas-datareader protobuf \
 && pip install --no-cache-dir wandb openai langchain_community langchain-huggingface huggingface_hub chromadb pymilvus opensearch-py pymupdf pdfminer pdfplumber pymupdf4llm pdfkit pypdf markdownify safetensors

# (권장) 요구사항 파일로 추가 파이썬 라이브러리 설치
COPY requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir -r /tmp/requirements.txt \
 && pip install torch torchvision torchao==0.14.1

# --- FlashAttention2 (flash-attn) 설치 ---
# flash-attn 빌드/동작에 CUDA toolkit(nvcc), ninja, packaging 필요
# 공식 설치: pip install flash-attn --no-build-isolation
# MAX_JOBS는 RAM 부족 시 컴파일 병렬 수 제한용
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}
ENV MAX_JOBS=4

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir packaging ninja \
 && (nvcc --version || (echo "ERROR: nvcc not found. flash-attn은 소스 빌드 시 CUDA toolkit(nvcc)이 필요합니다." && exit 1)) \
 && pip install --no-cache-dir flash-attn --no-build-isolation \
 && python -c "import flash_attn; print('flash_attn OK:', flash_attn.__version__)"

# Setup oh-my-zsh (for unsloth user)
ARG USERNAME=unsloth
ARG USER_HOME=/home/${USERNAME}

RUN git clone https://github.com/ohmyzsh/ohmyzsh.git ${USER_HOME}/.oh-my-zsh \
 && cp ${USER_HOME}/.oh-my-zsh/templates/zshrc.zsh-template ${USER_HOME}/.zshrc \
 && sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/g' ${USER_HOME}/.zshrc \
 && chown -R ${USERNAME}:${USERNAME} ${USER_HOME}/.oh-my-zsh ${USER_HOME}/.zshrc

# 런타임은 다시 unsloth 유저로
USER unsloth
ENV HOME=/home/unsloth
ENV SHELL=/usr/bin/zsh

# Unsloth 권장 작업 디렉토리(볼륨 마운트 대상) :contentReference[oaicite:2]{index=2}
WORKDIR /workspace/work

# 베이스 이미지의 entrypoint/cmd를 그대로 사용 (Jupyter/SSH 등)
ENTRYPOINT []