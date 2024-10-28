ARG BASE_IMAGE
FROM ${BASE_IMAGE}
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

ARG USER=rsnet
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV HOME /home/$USER

RUN conda install -c conda-forge --yes jupyterlab \
 && jupyter notebook --generate-config

RUN conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia

# # Create Python Library Environments
# ARG LIB_PYTHON
# ADD ${LIB_PYTHON} environment.yml
# RUN conda env update --file environment.yml \
#  && rm -rf environment.yml \
#  && conda clean -afy
 
# RUN jupyter serverextension enable --py jupyterlab --sys-prefix \
#  && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
#     @jupyterlab/application-extension @jupyterlab/apputils-extension @jupyterlab/codemirror-extension @jupyterlab/completer-extension \
#     @jupyterlab/console-extension @jupyterlab/csvviewer-extension @jupyterlab/docmanager-extension @jupyterlab/documentsearch-extension \
#     @jupyterlab/extensionmanager-extension @jupyterlab/filebrowser-extension @jupyterlab/fileeditor-extension @jupyterlab/help-extension \
#     @jupyterlab/htmlviewer-extension @jupyterlab/hub-extension @jupyterlab/imageviewer-extension @jupyterlab/inspector-extension \
#     @jupyterlab/javascript-extension @jupyterlab/json-extension @jupyterlab/launcher-extension @jupyterlab/logconsole-extension \
#     @jupyterlab/mainmenu-extension @jupyterlab/markdownviewer-extension @jupyterlab/mathjax2-extension @jupyterlab/notebook-extension \
#     @jupyterlab/pdf-extension @jupyterlab/rendermime-extension @jupyterlab/running-extension @jupyterlab/settingeditor-extension \
#     @jupyterlab/shortcuts-extension @jupyterlab/statusbar-extension @jupyterlab/terminal-extension \
#     @jupyterlab/theme-dark-extension @jupyterlab/theme-light-extension @jupyterlab/tooltip-extension @jupyterlab/ui-components-extension \
#     @jupyterlab/vdom-extension @jupyterlab/vega5-extension @jupyterlab/git @krassowski/jupyterlab-lsp 
# RUN jupyter labextension install jupyterlab-dash jupyterlab-interactive-dashboard-editor \
#  && jupyter lab build

RUN conda install -c conda-forge --yes nodejs=18
RUN jupyter labextension install --no-build @jupyter-widgets/jupyterlab-manager
#     @jupyterlab/application-extension @jupyterlab/apputils-extension @jupyterlab/codemirror-extension @jupyterlab/completer-extension \
#     @jupyterlab/console-extension @jupyterlab/csvviewer-extension @jupyterlab/docmanager-extension @jupyterlab/documentsearch-extension \
#     @jupyterlab/extensionmanager-extension @jupyterlab/filebrowser-extension @jupyterlab/fileeditor-extension @jupyterlab/help-extension \
#     @jupyterlab/htmlviewer-extension @jupyterlab/hub-extension @jupyterlab/imageviewer-extension @jupyterlab/inspector-extension \
#     @jupyterlab/javascript-extension @jupyterlab/json-extension @jupyterlab/launcher-extension @jupyterlab/logconsole-extension \
#     @jupyterlab/mainmenu-extension @jupyterlab/markdownviewer-extension @jupyterlab/mathjax2-extension @jupyterlab/notebook-extension \
#     @jupyterlab/pdf-extension @jupyterlab/rendermime-extension @jupyterlab/running-extension @jupyterlab/settingeditor-extension \
#     @jupyterlab/shortcuts-extension @jupyterlab/statusbar-extension @jupyterlab/terminal-extension \
#     @jupyterlab/theme-dark-extension @jupyterlab/theme-light-extension @jupyterlab/tooltip-extension @jupyterlab/ui-components-extension \
#     @jupyterlab/vdom-extension @jupyterlab/vega5-extension @jupyterlab/git @krassowski/jupyterlab-lsp

# RUN jupyter labextension install jupyterlab-dash jupyterlab-interactive-dashboard-editor
# RUN jupyter lab build

# USER root
# RUN sudo mkdir /notebook \
#  && chown $UID.$GID /notebook

# # SSH Server
# RUN ssh-keygen -A \
#  && service ssh start

# CMD ["sudo", "service", "ssh", "start"]

# Set notebook
USER $USER
VOLUME /notebook
WORKDIR /notebook
EXPOSE 8888
