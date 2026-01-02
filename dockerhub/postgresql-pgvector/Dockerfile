ARG IMAGE_BASE=bitnami/postgresql:17.0.0
FROM ${IMAGE_BASE}

# 루트 사용자로 전환하여 패키지 설치 및 pgvector 설치
USER root

# 필요한 패키지 설치
RUN install_packages git build-essential postgresql-server-dev-all

# 작업 디렉토리를 루트 사용자가 쓰기 가능한 위치로 설정
WORKDIR /tmp

# pgvector 클론 및 설치
ARG VERSION_PGVECTOR=v0.7.4
RUN git clone --branch ${VERSION_PGVECTOR} https://github.com/pgvector/pgvector \
 && cd pgvector \
 && make \
 && make install \
 && cd .. \
 && rm -rf pgvector

 # PostgreSQL 데이터 디렉토리의 소유권을 비트나미 사용자로 변경
RUN chown -R 1001:1001 /bitnami/postgresql

 # 불필요한 패키지 제거
RUN apt-get remove -y git build-essential postgresql-server-dev-all && \
apt-get autoremove -y && \
apt-get clean

# 기본 비루트 사용자로 다시 전환
USER 1001

# 포트 공개
EXPOSE 5432

