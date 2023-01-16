ARG BASE_IMAGE
FROM ${BASE_IMAGE}
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

# Install system packages
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TZ=Asia/Seoul
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing
RUN apt-get upgrade -y
RUN apt-get install -yq --no-install-recommends wget ca-certificates sudo locales tzdata
RUN apt-get autoclean && apt-get autoremove
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen

# Create a non-root user
ARG USER=kwp
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV HOME /home/$USER
RUN groupadd --gid $USER_GID $USER \
 && useradd --uid $USER_UID --gid $USER_GID -m $USER \
 && echo $USER ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER \
 && chmod 0440 /etc/sudoers.d/$USER

USER $USER
WORKDIR $HOME

# Install Miniconda
ARG VERSION_MINICONDA=latest
ARG VERSION_PYTHON=3.9
ENV CONDA_DIR $HOME/miniconda3
ENV PATH=${CONDA_DIR}/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${VERSION_MINICONDA}-Linux-x86_64.sh -O ~/miniconda.sh \
 && chmod +x ~/miniconda.sh \
 && /bin/bash ~/miniconda.sh -b -u -p $CONDA_DIR \
 && rm ~/miniconda.sh \
 && echo . ${CONDA_DIR}/etc/profile.d/conda.sh >> ~/.bashrc \
 && echo conda activate base >> ~/.bashrc \
 && conda init bash \
 && . ~/.bashrc \
 && conda install -y libgcc tini python=${VERSION_PYTHON} \
 && conda config --system --prepend channels conda-forge \
 && conda update --all -y \
 && conda clean -afy
