#!/bin/bash

echo "[INFO] Copying backend.env to /home/ubuntu/wavetowww/source/server/app/.env"
cp /home/ubuntu/env-configs/backend.env /home/ubuntu/wavetowww/source/server/app/.env

echo "[INFO] Copying kernel.env to /home/ubuntu/wavetowww/source/kernel/.env"
cp /home/ubuntu/env-configs/kernel.env /home/ubuntu/wavetowww/source/kernel/.env

echo "[INFO] All .env files copied successfully."
