ARG VERSION_BASE
FROM registry.k3s.lab/miniconda-gpu-devel:${VERSION_BASE}
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

RUN conda install -c conda-forge --yes jupyterlab \
 && jupyter notebook --generate-config

# Create Python Library Environments
ARG LIB_PYTHON
ADD ${LIB_PYTHON}.yml environment.yml
RUN conda env update --file environment.yml \
 && rm -rf environment.yml

RUN jupyter serverextension enable --py jupyterlab --sys-prefix \
 && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
    @jupyterlab/application-extension @jupyterlab/apputils-extension @jupyterlab/codemirror-extension @jupyterlab/completer-extension \
    @jupyterlab/console-extension @jupyterlab/csvviewer-extension @jupyterlab/docmanager-extension @jupyterlab/documentsearch-extension \
    @jupyterlab/extensionmanager-extension @jupyterlab/filebrowser-extension @jupyterlab/fileeditor-extension @jupyterlab/help-extension \
    @jupyterlab/htmlviewer-extension @jupyterlab/hub-extension @jupyterlab/imageviewer-extension @jupyterlab/inspector-extension \
    @jupyterlab/javascript-extension @jupyterlab/json-extension @jupyterlab/launcher-extension @jupyterlab/logconsole-extension \
    @jupyterlab/mainmenu-extension @jupyterlab/markdownviewer-extension @jupyterlab/mathjax2-extension @jupyterlab/notebook-extension \
    @jupyterlab/pdf-extension @jupyterlab/rendermime-extension @jupyterlab/running-extension @jupyterlab/settingeditor-extension \
    @jupyterlab/shortcuts-extension @jupyterlab/statusbar-extension @jupyterlab/terminal-extension \
    @jupyterlab/theme-dark-extension @jupyterlab/theme-light-extension @jupyterlab/tooltip-extension @jupyterlab/ui-components-extension \
    @jupyterlab/vdom-extension @jupyterlab/vega5-extension @jupyterlab/git @krassowski/jupyterlab-lsp

USER root
RUN sudo mkdir /notebooks \
 && chown $UID.$GID /notebooks

# SSH Server
RUN ssh-keygen -A \
 && service ssh start
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]

# notebook setting
USER $USER
VOLUME /notebooks
WORKDIR /notebooks

