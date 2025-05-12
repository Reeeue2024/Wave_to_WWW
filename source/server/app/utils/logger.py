# [ Server ] logger.py

import logging
import os

# 로그 디렉토리 및 파일 준비
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "server.log")
os.makedirs(LOG_DIR, exist_ok=True)

# 로거 생성
logger = logging.getLogger("phishing_logger")
logger.setLevel(logging.INFO)

# 포맷 정의
formatter = logging.Formatter("[%(asctime)s] %(levelname)-8s %(message)s")

# 파일 핸들러
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 콘솔 핸들러 (선택)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
