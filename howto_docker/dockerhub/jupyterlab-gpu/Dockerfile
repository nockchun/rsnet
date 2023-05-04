ARG BASE_IMAGE
FROM ${BASE_IMAGE}
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

ARG USER=rsnet
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV HOME /home/$USER

RUN conda install -c conda-forge --yes jupyterlab \
 && jupyter notebook --generate-config

# Create Python Library Environments
ARG LIB_PYTHON
ADD ${LIB_PYTHON} environment.yml
RUN conda env update --file environment.yml \
 && rm -rf environment.yml \
 && conda clean -afy

# Create Tensorflow Environments
RUN sudo apt-get upgrade -y \
 && sudo apt-get install libcudnn8-dev -y \
 && sudo apt-get autoclean && sudo apt-get autoremove
RUN conda install -c conda-forge jupyterlab-lsp python-lsp-server
RUN pip install tensorflow-gpu==2.11.0

# Set notebook
EXPOSE 8888
USER $USER
VOLUME /notebook
WORKDIR /notebook
