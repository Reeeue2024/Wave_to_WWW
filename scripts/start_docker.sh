#!/bin/bash
set -e

# 루트 경로 계산
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

# 멀티 컨테이너 재시작
docker-compose -f "$PROJECT_ROOT/source/docker-compose.yml" start
