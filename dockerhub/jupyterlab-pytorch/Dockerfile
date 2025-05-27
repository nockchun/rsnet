# Use CUDA 12.4
ARG IMAGE_BASE
FROM ${IMAGE_BASE}
SHELL ["/bin/bash", "-c"]
ENV SHELL=/bin/bash
ENV DEBIAN_FRONTEND=noninteractive

# Export paths for CUDA and cuDNN
ENV CUDA_HOME=/usr/local/cuda
ENV PATH="/usr/local/cuda/bin:$PATH"
ENV CPATH="/usr/local/cuda/include:/usr/include:$CPATH"
ENV LIBRARY_PATH="/usr/local/cuda/lib64:$LIBRARY_PATH"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH"

RUN echo 'command -v nvcc &>/dev/null && nvcc -V || uname -srm' >> /root/.bashrc && \
    echo 'eval "$(starship init bash)"' >> /root/.bashrc

# Install basic packages
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt-get update --fix-missing \
 && apt-get upgrade -y \
 && apt-get install -yq --no-install-recommends debconf apt wget git curl bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 tree \
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


# Install Conda Environment
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/install.sh && \
    bash ~/install.sh -b -p /root/conda && rm ~/install.sh && \
    eval "$('/root/conda/bin/conda' 'shell.bash' 'hook')" && conda init

# Create Development Environment
ENV PATH="/root/conda/bin:$PATH"
RUN conda create -n torch python=3.12 anaconda -y && \
    conda clean -a && pip cache purge

# Setup JupyterLab plugins
RUN eval "$('/root/conda/bin/conda' 'shell.bash' 'hook')" && conda activate torch && \
    conda install -c conda-forge starship nodejs pandoc texlive-core texlab chktex && \
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
COPY JupyterLabConfig/notebooks/ /root/projects/demo_notebooks/
COPY JupyterLabConfig/starship.toml /root/.config/starship.toml

# Install PyTorch and AI libs
RUN eval "$('/root/conda/bin/conda' 'shell.bash' 'hook')" && conda activate torch \
 && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 \
 && conda clean -a && pip cache purge

RUN eval "$('/root/conda/bin/conda' 'shell.bash' 'hook')" && conda activate torch \
 && pip install --no-cache-dir opencv-python gym gymnasium gymnasium[classic-control] deap evaluate pygad gymnasium[atari,accept-rom-license] gymnasium[box2d] gym-notebook-wrapper ray[all] tables nengo[all] lz4 nltk poetry tsaug seasonal pydot einops typing-extensions \
    python-kubernetes pyts dash tortoise-orm html5lib more-itertools httplib2 celery psycopg2 asyncpg tqdm asyncio nest-asyncio werkzeug==3.1\
 && pip install --no-cache-dir danbi ta pandas-ta selenium backtrader yfinance transitions plotly filterpy orjson nats-py dbutils \
 && conda clean -a && pip cache purge

RUN eval "$('/root/conda/bin/conda' 'shell.bash' 'hook')" && conda activate torch \
 && pip install --no-cache-dir huggingface_hub datasets transformers==4.52.3 xformers==0.0.30 bitsandbytes peft accelerate wandb sentence-transformers trl==0.17.0 \
    # openai langchain_community faiss-gpu chromadb streamlit gradio auto_gptq autoawq optimum autotrain-advanced pymilvus opensearch-py \
    # langchain langchain-core langchain-text-splitters langchain-openai langchain-milvus langchain-docling  langchain-docling langchain-milvus langchain-qdrant langchain-chroma langchain-ollama bs4 langgraph \
    # pymupdf pdfminer pdfplumber flash-attn pymupdf4llm pdfkit markdownify unsloth \
 && conda clean -a && pip cache purge

# Run JupyterLab on start
ENV DEBIAN_FRONTEND=dialog
RUN echo 'conda activate torch' >> /root/.bashrc && \
    echo 'jupyter lab' > /root/entrypoint.sh

WORKDIR /root/projects
ENTRYPOINT ["/bin/bash", "-i", "/root/entrypoint.sh"]
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
CMD curl -f -s http://localhost:80/torch || exit 1


