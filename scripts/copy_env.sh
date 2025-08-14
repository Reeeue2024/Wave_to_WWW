#!/bin/bash

echo "[INFO] Creating target directories..."
mkdir -p source/server/app
mkdir -p source/kernel

echo "[INFO] Copying backend.env to source/server/app/.env"
cp /home/ubuntu/env-configs/backend.env source/server/app/.env

echo "[INFO] Copying kernel.env to source/kernel/.env"
cp /home/ubuntu/env-configs/kernel.env source/kernel/.env

echo "[INFO] All .env files copied to CodeDeploy archive directory."
