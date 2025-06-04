#!/bin/bash
set -e

# 루트 경로 계산
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

# 실행 중인 컨테이너 상태 출력
docker-compose -f "$PROJECT_ROOT/source/docker-compose.yml" ps

# 최대 시도 횟수와 대기 시간 설정
MAX_ATTEMPTS=30
WAIT_SECONDS=10
ATTEMPT=1

echo "서비스 헬스체크 시작..."

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "시도 $ATTEMPT/$MAX_ATTEMPTS..."
    
    # 타임아웃 5초로 헬스체크 실행
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 5 http://localhost:80)
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo "서비스 정상 작동 중 (HTTP 200)"
        exit 0
    else
        echo "서비스 응답 코드: $HTTP_CODE, ${WAIT_SECONDS}초 후 재시도..."
        sleep $WAIT_SECONDS
        ATTEMPT=$((ATTEMPT + 1))
    fi
done

echo "서비스 시작 실패 - 최대 시도 횟수 초과"
exit 1
