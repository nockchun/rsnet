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
 && apt-get install -yq --no-install-recommends debconf apt wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 \
    tzdata fonts-liberation fonts-nanum* net-tools vim openssh-client graphviz libgraphviz-dev libgl1-mesa-glx libhdf5-dev openmpi-bin pandoc run-one \
    autoconf automake dpkg-dev file build-essential g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev cmake \
    libevent-dev libffi-dev libgdbm-dev libgeoip-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev htop cm-super dvipng \
    libmagickcore-dev libmagickwand-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev xvfb less libtcmalloc-minimal4 \
    libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev \
    iputils-ping dnsutils language-pack-ko ffmpeg openjdk-17-jre-headless libatlas-base-dev libgflags-dev inkscape texlive texlive-xetex texlive-fonts-recommended texlive-plain-generic \
    texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science tipa \
    libgoogle-glog-dev libhdf5-serial-dev libleveldb-dev liblmdb-dev libprotobuf-dev libsnappy-dev protobuf-compiler ghostscript python3-tk python3-dev \
    software-properties-common gpg librdmacm1 libibverbs1 ibverbs-providers openssh-server supervisor libcudnn8-dev tini \
    sox libcairo2-dev libpango1.0-dev libboost-all-dev swig libarchive-dev zsh libnuma-dev wkhtmltopdf \
 && apt autoremove \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
 && bash /tmp/miniconda.sh -b -p /opt/conda \
 && rm /tmp/miniconda.sh \
 && /opt/conda/bin/conda clean -afy

ARG VERSION_PYTHON
ARG VERSION_NUMPY
RUN conda update -n base -c defaults conda \
 && conda config --add channels conda-forge \
 && conda config --set channel_priority strict \
 && conda install -y -n base -c conda-forge python=${VERSION_PYTHON} numpy ipykernel ipywidgets ipytest ipympl \
    jupyter_bokeh statsmodels graphviz pyopencl scikit-learn sentencepiece pykalman gplearn \
    pillow firefox geckodriver apscheduler scipy pandas pandas-profiling pandas-datareader \
 && conda clean -afy

# Setup JupyterLab plugins
RUN conda install -c conda-forge starship nodejs pandoc texlive-core texlab chktex && \
    pip install 'jupyterlab>=4.1.0,<5.0.0a0' jupyterlab-lsp 'python-lsp-server[all]' \
        jupyterlab-code-formatter black isort jupyterlab-spellchecker jupyterlab-latex \
        jupyter-resource-usage jupyterlab_execute_time lckr_jupyterlab_variableinspector \
        jupyterlab-git jupyterlab_wakatime 'ipywidgets>=8.0' && \
    npm set prefix /root && npm install -g --save-dev remark-language-server \
        remark-preset-lint-consistent remark-preset-lint-recommended && \
    jupyter labextension disable "@jupyterlab/apputils-extension:announcements" && \
    conda clean -a && pip cache purge && npm cache clean --force

COPY JupyterLabConfig/jupyter_lab_config.py /root/.jupyter/jupyter_lab_config.py
COPY JupyterLabConfig/extensions/ /root/.jupyter/lab/user-settings/\@jupyterlab/
COPY JupyterLabConfig/jupyterlab-lsp/ /root/.jupyter/lab/user-settings/\@jupyter-lsp/jupyterlab-lsp/
COPY JupyterLabConfig/jupyterlab-lsp/unified_language_server.py /root/conda/envs/lab/lib/python3.12/site-packages/jupyter_lsp/specs/unified_language_server.py
COPY JupyterLabConfig/jupyterlab-lsp/remarkrc.yml /root/.remarkrc.yml
COPY JupyterLabConfig/starship.toml /root/.config/starship.toml

# Install PyTorch
ARG VERSION_PYTORCH
# RUN conda install -y -n base pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.4 -c pytorch -c nvidia \
#     && conda clean -afy
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Install Tensorflow
# ARG VERSION_TF
# ENV TF_GPU_THREAD_MODE=gpu_shared \
#     TF_FORCE_GPU_ALLOW_GROWTH=true \
#     TF_ENABLE_ONEDNN_OPTS=0 \
#     TF_CPP_MIN_LOG_LEVEL=3
# RUN pip install --no-cache-dir tensorflow==${VERSION_TF} tensorflow-datasets tensorflow-probability tensorflow-addons nvidia-pyindex tf-keras

# Install Extra Library
RUN pip install --no-cache-dir opencv-python gym gymnasium gymnasium[classic-control] deap evaluate pygad gymnasium[atari,accept-rom-license] gymnasium[box2d] gym-notebook-wrapper ray[all] tables nengo[all] lz4 nltk poetry tsaug seasonal pydot einops typing-extensions \
    python-kubernetes pyts dash tortoise-orm html5lib more-itertools httplib2 celery psycopg2 asyncpg tqdm asyncio nest-asyncio werkzeug==3.1\
 && pip install --no-cache-dir danbi ta pandas-ta selenium backtrader yfinance transitions plotly filterpy orjson nats-py dbutils

RUN pip install --no-cache-dir huggingface_hub datasets transformers==4.52.3 xformers==0.0.30 bitsandbytes peft accelerate wandb sentence-transformers trl==0.17.0 \
    openai langchain_community faiss-gpu chromadb streamlit gradio auto_gptq autoawq optimum autotrain-advanced pymilvus opensearch-py \
    langchain langchain-core langchain-text-splitters langchain-openai langchain-milvus langchain-docling  langchain-docling langchain-milvus langchain-qdrant langchain-chroma langchain-ollama bs4 langgraph \
    pymupdf pdfminer pdfplumber flash-attn pymupdf4llm pdfkit markdownify unsloth

# Setup oh-my-zsh
RUN git clone https://github.com/ohmyzsh/ohmyzsh.git /root/.oh-my-zsh \
 && cp /root/.oh-my-zsh/templates/zshrc.zsh-template /root/.zshrc \
 && sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/g' /root/.zshrc
ENV SHELL=/usr/bin/zsh
ENTRYPOINT ["/usr/bin/zsh", "-c", "exec \"$@\"", "--"]

# Expose JupyterLab default port
EXPOSE 8888
