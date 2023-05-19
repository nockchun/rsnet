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
# RUN conda install -c conda-forge cudatoolkit cudnn tensorflow-gpu
RUN pip install tensorrt tensorflow-gpu==2.10.0
# RUN conda install -c anaconda tensorflow-gpu

# Set notebook
EXPOSE 8888
USER $USER
VOLUME /notebook
WORKDIR /notebook
