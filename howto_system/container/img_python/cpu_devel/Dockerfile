ARG BASE_IMAGE
FROM ${BASE_IMAGE}
LABEL maintainer="RealStudy.NET <nockchun@gmail.com>"

# Create Python Library Environments
ARG LIB
ADD ${LIB} environment.yml
RUN conda env update --file environment.yml \
 && rm -rf environment.yml
