ARG BASE_IMAGE
FROM ${BASE_IMAGE}
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

ARG USER=rsnet
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV HOME /home/$USER

# Create Python Library Environments
ARG LIB_PYTHON
ADD ${LIB_PYTHON} environment.yml
RUN conda env update --file environment.yml \
 && rm -rf environment.yml \
 && conda clean -afy

# Create Tensorflow Environments
ARG TF_VERSION
RUN pip install tensorrt tensorflow-gpu==${TF_VERSION}

# Create Jupyterlab Environments
RUN conda install -c conda-forge --yes jupyterlab \
 && jupyter lab --generate-config
RUN pip install jupyterlab-lsp python-lsp-server jupyter_console jupyter_contrib_nbextensions jupyter_nbextensions_configurator \
    jupyterlab-git jupyterlab-drawio jupyter_bokeh jupyterlab-lsp jupyterlab-dash ipykernel ipywidgets ipytest ipympl jupyterlab jupyterlab-interactive-dashboard-editor

# Set notebook
EXPOSE 8888
USER $USER
VOLUME /notebook
WORKDIR /notebook
