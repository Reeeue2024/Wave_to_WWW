#!/bin/bash
set -e

echo "배포 스크립트 시작..."

# 루트 경로 계산
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

# AWS ECR 로그인
echo "ECR 로그인 시도..."
if ! aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 589744711132.dkr.ecr.ap-northeast-2.amazonaws.com; then
    echo "ECR 로그인 실패"
    exit 1
fi
echo "ECR 로그인 성공"

# 이미지 최신 상태로 pull
echo "도커 이미지 pull 시도..."
if ! docker-compose -f "$PROJECT_ROOT/source/docker-compose.yml" pull; then
    echo "도커 이미지 pull 실패"
    exit 1
fi
echo "도커 이미지 pull 성공"

# 컨테이너 백그라운드 실행
echo "도커 컨테이너 실행 시도..."
if ! docker-compose -f "$PROJECT_ROOT/source/docker-compose.yml" up -d; then
    echo "도커 컨테이너 실행 실패"
    exit 1
fi
echo "도커 컨테이너 실행 성공"

echo "배포 스크립트 완료"