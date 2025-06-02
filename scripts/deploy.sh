#!/bin/bash

# AWS ECR 로그인
$(aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 589744711132.dkr.ecr.ap-northeast-2.amazonaws.com)

# 기존 도커 컨테이너 중지 및 삭제
docker stop wavetowww-container || true
docker rm wavetowww-container || true

# 새 도커 이미지 풀 (GitHub Actions가 푸시해둔 이미지)
docker pull 589744711132.dkr.ecr.ap-northeast-2.amazonaws.com/wavetowww:latest

# 컨테이너 실행 (백그라운드 모드, 환경변수 추가 가능)
docker run -d --name wavetowww-container -p 80:80 589744711132.dkr.ecr.ap-northeast-2.amazonaws.com/wavetowww:latest
