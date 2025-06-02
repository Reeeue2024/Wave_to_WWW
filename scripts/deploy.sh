#!/bin/bash

# 기존 도커 컨테이너 중지 및 삭제
docker stop wavetowww-container || true
docker rm wavetowww-container || true

# 새 도커 이미지 풀 (GitHub Actions가 푸시해둔 이미지)
docker pull <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/wavetowww:latest

# 컨테이너 실행 (백그라운드 모드, 환경변수 추가 가능)
docker run -d --name wavetowww-container -p 80:80 <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/wavetowww:latest
