FROM alpine
LABEL maintainer="Jaehong. Kim. <nockchun@gmail.com>"

# Install system packages
RUN sed -i 's/archive.ubuntu.com/ftp.harukasan.org/g' /etc/apt/sources.list \
 && apt clean && apt update && apt install -yq --no-install-recommends apt-utils \
      ca-certificates sudo bzip2 gcc g++ make git wget curl vim net-tools openssh-server \
      sudo cmake \
 && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen

# Setting up container startup
ENTRYPOINT ["tini", "-g", "--"]

USER $NB_USER
WORKDIR /notebooks
