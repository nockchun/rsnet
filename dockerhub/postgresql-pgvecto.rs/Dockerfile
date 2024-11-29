ARG IMAGE_BASE=bitnami/postgresql:17.0.0
FROM ${IMAGE_BASE} AS builder

USER root
COPY vectors-pg17_0.4.0_amd64.deb /tmp
RUN apt-get install /tmp/vectors-pg17_0.4.0_amd64.deb

FROM ${IMAGE_BASE}
USER root
COPY --from=builder /usr/lib/postgresql/17/lib/vectors.so /opt/bitnami/postgresql/lib
COPY --from=builder /usr/share/postgresql/17/extension/* /opt/bitnami/postgresql/share/extension/
USER 1001
