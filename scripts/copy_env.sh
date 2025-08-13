#!/bin/bash

echo "[INFO] Copying backend.env to server/app/.env"
cp /home/ubuntu/env-configs/backend.env /home/ubuntu/app/source/server/app/.env

echo "[INFO] Copying kernel.env to kernel/.env"
cp /home/ubuntu/env-configs/kernel.env /home/ubuntu/app/source/kernel/.env

echo "[INFO] All .env files copied successfully."
