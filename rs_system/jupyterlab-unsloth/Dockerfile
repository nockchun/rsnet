# syntax=docker/dockerfile:1.7

# 원하는 Unsloth 태그로 고정하고 싶으면 빌드 시 BASE_IMAGE를 바꾸세요.
# 예: unsloth/unsloth:2025.11.2-pt2.8.0-cu12.8-trans4.57.0  (Docker Hub / GHCR에 존재)
ARG BASE_IMAGE=unsloth/unsloth:latest
FROM ${BASE_IMAGE}

# Unsloth 컨테이너는 기본적으로 non-root(unsloth) 유저로 실행됩니다. :contentReference[oaicite:1]{index=1}
# 이미지 빌드 단계에서 패키지 설치를 위해 root로 전환합니다.
USER root

# (선택) 시스템 의존성 설치: 필요 없으면 이 블록 제거하세요.
# - build-essential: 일부 pip 패키지 빌드에 필요
# - git/curl: 소스 설치/다운로드용
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
      git curl ca-certificates build-essential \
    && rm -rf /var/lib/apt/lists/*

# (권장) 요구사항 파일로 추가 파이썬 라이브러리 설치
COPY requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir -r /tmp/requirements.txt

# 런타임은 다시 unsloth 유저로
USER unsloth

# Unsloth 권장 작업 디렉토리(볼륨 마운트 대상) :contentReference[oaicite:2]{index=2}
WORKDIR /workspace/work

# 베이스 이미지의 entrypoint/cmd를 그대로 사용 (Jupyter/SSH 등)
