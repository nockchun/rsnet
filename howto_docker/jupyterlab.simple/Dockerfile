FROM tensorflow/tensorflow:2.2.0-gpu
LABEL maintainer="Jaehong. Kim. <nockchun@gmail.com>"

# Install system packages
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list \
 && apt clean && apt update && apt install -yq --no-install-recommends apt-utils \
    ca-certificates sudo locales bzip2 gcc g++ make git graphviz libgl1-mesa-glx libhdf5-dev openmpi-bin wget curl npm \
    vim net-tools openssh-server sudo cmake zlib1g-dev libjpeg-dev xvfb xorg-dev xcftools unzip \
    libpng-dev libtiff5 libtiff5-dev xvfb xserver-xephyr vnc4server python-opengl \
 && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen

# # Install Fonts
RUN apt install -y unzip fonts-unfonts-core fonts-unfonts-extra fonts-baekmuk fonts-nanum fonts-nanum-coding fonts-nanum-extra \
 && wget https://github.com/naver/d2codingfont/releases/download/VER1.21/D2Coding-1.2.zip \
 && mkdir /usr/share/fonts/truetype/D2Coding \
 && unzip D2Coding-1.2.zip -d /usr/share/fonts/truetype/D2Coding/ \
 && rm -rf /usr/share/fonts/truetype/D2Coding/__MACOSX \
 && fc-cache -f -v

# Create Jupyterlab Environments
RUN pip install --upgrade pip setuptools jupyterlab==1.2.0 \
 && jupyter notebook --generate-config \
 && jupyter serverextension enable --py jupyterlab --sys-prefix \
 && jupyter labextension install @jupyter-widgets/jupyterlab-manager @jupyterlab/application-extension @jupyterlab/apputils-extension \
    @jupyterlab/extensionmanager-extension @jupyterlab/filebrowser-extension @jupyterlab/fileeditor-extension @jupyterlab/help-extension \
    @jupyterlab/imageviewer-extension @jupyterlab/inspector-extension @jupyterlab/json-extension @jupyterlab/launcher-extension @jupyterlab/logconsole-extension \
    @jupyterlab/markdownviewer-extension @jupyterlab/mathjax2-extension @jupyterlab/pdf-extension @jupyterlab/settingeditor-extension \
    @jupyterlab/shortcuts-extension @jupyterlab/statusbar-extension @jupyterlab/tabmanager-extension @jupyterlab/terminal-extension \
    @jupyterlab/theme-dark-extension @jupyterlab/theme-light-extension @jupyterlab/tooltip-extension @jupyterlab/ui-components-extension \
    kubeflow-kale-launcher \
 && jupyter labextension install jupyter-matplotlib @jupyterlab/fasta-extension @jupyterlab/toc @jupyterlab/mathjax3-extension \
    @jupyterlab/geojson-extension @jupyterlab/katex-extension @lckr/jupyterlab_variableinspector

# Install Required Library
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt \
 && rm requirements.txt

# Tini: https://github.com/krallin/tini
RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

# Setting up container startup
EXPOSE 8888
EXPOSE 6006
VOLUME /notebooks
RUN chown -R $NB_USER.$NB_USER /notebooks

USER $NB_USER
ENTRYPOINT ["tini", "-g", "--"]
CMD ["sh","-c", "jupyter lab --notebook-dir=/home/jovyan --ip=0.0.0.0 --no-browser --allow-root --port=8888 --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' --NotebookApp.base_url=${NB_PREFIX}"]
