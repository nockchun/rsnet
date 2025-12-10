ARG IMAGE_BASE
FROM ${IMAGE_BASE}

# [STEP 1: 빌더 스테이지]
FROM ${IMAGE_BASE} AS builder

USER root

# 빌드 도구 + pgrx에 필요한 의존성
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-server-dev-18 \
    git \
    curl \
    ca-certificates \
    pkg-config \
    libssl-dev \
    jq \
    clang \
    && rm -rf /var/lib/apt/lists/*

# Rust 설치
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# pgvectorscale 소스
RUN git clone https://github.com/timescale/pgvectorscale.git /tmp/pgvectorscale

# 레포 구조상 실제 크레이트 디렉터리로 이동
WORKDIR /tmp/pgvectorscale/pgvectorscale

# 레포가 쓰는 pgrx 버전에 맞춰 cargo-pgrx 설치 (공식 README 방식)
RUN cargo install --locked cargo-pgrx --version \
    $(cargo metadata --format-version 1 | jq -r '.packages[] | select(.name == "pgrx") | .version')

# 시스템에 이미 있는 PG18의 pg_config를 명시
RUN cargo pgrx init --pg18 /usr/lib/postgresql/18/bin/pg_config

# 여기서 .so/.control/.sql이 "정상 설치 경로"로 들어감
RUN cargo pgrx install --release --pg-config /usr/lib/postgresql/18/bin/pg_config

# [STEP 2: 실행 스테이지]
FROM ${IMAGE_BASE}

USER root

# 빌더에서 '설치된 결과물'만 가져오기
COPY --from=builder /usr/lib/postgresql/18/lib/vectorscale* /usr/lib/postgresql/18/lib/
COPY --from=builder /usr/share/postgresql/18/extension/vectorscale* /usr/share/postgresql/18/extension/
COPY ./initdb/020_enable_vectorscale.sh /docker-entrypoint-initdb.d/020_enable_vectorscale.sh

USER postgres
