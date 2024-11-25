FROM tensorchord/pgvecto-rs-binary:pg17-v0.4.0-amd64 as binary
FROM bitnami/postgresql:17.1.0

USER root
COPY --from=binary /pgvecto-rs-binary-release.deb /tmp/vectors.deb
RUN apt-get install -y /tmp/vectors.deb && rm -f /tmp/vectors.deb
USER 1001

CMD ["postgres", "-c" ,"shared_preload_libraries=vectors.so", "-c", "search_path=\"$user\", public, vectors", "-c", "logging_collector=on"]