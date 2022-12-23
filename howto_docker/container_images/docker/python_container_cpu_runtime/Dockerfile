ARG VERSION_BASE
FROM ${VERSION_BASE}
LABEL maintainer="Kim. Jaehong. <nockchun@ahnlab.com>"
 
# Create Python Library Environments
ARG LIB_PYTHON
ADD ${LIB_PYTHON}.yml environment.yml
RUN conda env update --file environment.yml && conda update --all -y && conda upgrade celery --all -y \
 && rm -rf environment.yml && conda clean -afy
