#!/bin/bash

cd /home/ubuntu/wavetowww/

# 멀티 컨테이너 모두 중지 및 제거
docker-compose -f source/docker-compose.yml down
