#!/bin/bash

cd /home/ubuntu/wavetowww/

# 이미 실행 중인 컨테이너를 재시작
docker-compose -f source/docker-compose.yml start
