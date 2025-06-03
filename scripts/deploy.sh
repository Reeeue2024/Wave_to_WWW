#!/bin/bash

# AWS ECR 로그인
$(aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 589744711132.dkr.ecr.ap-northeast-2.amazonaws.com)

# 루트 경로 계산
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

# 이미지 최신 상태로 pull
docker-compose -f "$PROJECT_ROOT/source/docker-compose.yml" pull

# 컨테이너 백그라운드 실행
docker-compose -f "$PROJECT_ROOT/source/docker-compose.yml" up -d