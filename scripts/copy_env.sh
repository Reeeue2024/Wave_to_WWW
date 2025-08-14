#!/bin/bash

echo "[INFO] Copying .env files to deployment archive..."

cp /home/ubuntu/env-configs/backend.env /opt/codedeploy-agent/deployment-root/*/deployment-archive/source/server/app/.env
cp /home/ubuntu/env-configs/kernel.env /opt/codedeploy-agent/deployment-root/*/deployment-archive/source/kernel/.env

echo "[INFO] .env files successfully copied into CodeDeploy archive"
