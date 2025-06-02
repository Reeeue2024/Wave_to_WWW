#!/bin/bash

# AWS ECR 로그인
$(aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 589744711132.dkr.ecr.ap-northeast-2.amazonaws.com)

# 작업 디렉토리 이동 (appspec.yml의 destination 경로에 맞게 조정)
cd /home/ubuntu/wavetowww/

# 이미지 최신 상태로 풀기
docker-compose -f source/docker-compose.yml pull

# 컨테이너(서비스) 백그라운드 실행
docker-compose -f source/docker-compose.yml up -d