ARG VERSION_CUDA
FROM nvidia/cuda:${VERSION_CUDA}
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

# Install system packages
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TZ=Asia/Seoul
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing
RUN apt-get upgrade -y
RUN apt-get install -yq --no-install-recommends wget ca-certificates sudo locales
RUN apt-get autoclean && apt-get autoremove
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen
#RUN rm -rf /bin/sh && ln -s /bin/bash /bin/sh

# Create a non-root user
ARG USERNAME=rsnet
ARG PASSWORD=rsnet
ARG UID=1000
ARG GID=1000
ENV USER $USERNAME
ENV UID $UID
ENV GID $GID
ENV HOME /home/$USER

RUN groupadd -g $GID $USER && adduser --disabled-password --gecos "Non-root user" --uid $UID --gid $GID --home $HOME $USER && echo $USER:$PASSWORD | chpasswd && adduser $USER sudo && echo $USER 'ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && usermod -a -G $USER $USER

USER $USER
WORKDIR $HOME

# Install Miniconda
ARG VERSION_MINICONDA=latest
ARG VERSION_PYTHON=3.9
ENV CONDA_DIR $HOME/miniconda3
ENV PATH=${CONDA_DIR}/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${VERSION_MINICONDA}-Linux-x86_64.sh -O ~/miniconda.sh && chmod +x ~/miniconda.sh && ~/miniconda.sh -b -u -p $CONDA_DIR && rm ~/miniconda.sh && conda install -y libgcc tini python=${VERSION_PYTHON} && conda install -c conda-forge xorg-libx11 && conda config --system --prepend channels conda-forge && conda update --all -y && conda init bash && conda clean -afy
