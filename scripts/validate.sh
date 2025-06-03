#!/bin/bash
set -e

# 루트 경로 계산
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

# 실행 중인 컨테이너 상태 출력
docker-compose -f "$PROJECT_ROOT/source/docker-compose.yml" ps

# 웹서비스 HTTP 상태코드 확인
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80)

if [ "$HTTP_CODE" == "200" ]; then
  echo "서비스 정상 작동 중 (HTTP 200)"
  exit 0
else
  echo "서비스 이상 발생 (HTTP 코드: $HTTP_CODE)"
  exit 1
fi
