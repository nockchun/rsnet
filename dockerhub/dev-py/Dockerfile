ARG VERSION_BASE
FROM ${VERSION_BASE}
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

# Create Python Library Environments
ARG LIB_PYTHON
ADD ${LIB_PYTHON}.yml environment.yml
RUN conda env update --file environment.yml \
 && rm -rf environment.yml \
 && conda clean -afy
ADD require.yml require.yml
RUN conda env update --file require.yml \
 && rm -rf require.yml \
 && conda clean -afy

# SSH Server
RUN sudo ssh-keygen -A \
 && sudo service ssh start
EXPOSE 22

CMD ["sudo", "/usr/sbin/sshd", "-D"]
