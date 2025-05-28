# [ Configs ] config.py
# source/server/server_config/config.py

import os
from dotenv import load_dotenv
from pathlib import Path

# .env 파일 경로 지정 (이 파일 기준 상대경로)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# 환경변수 로드 및 변환
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "")
API_VERSION = os.getenv("API_VERSION", "v1")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
