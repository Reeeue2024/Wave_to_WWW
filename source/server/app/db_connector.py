# [ Server ] db_connector.py
# source/server/app/db_connector.py

import mysql.connector
import logging
from dotenv import load_dotenv
import os

# 환경변수 로드
load_dotenv()

# 로깅 설정
logger = logging.getLogger(__name__)

# DB 접속 설정
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# DB 연결
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Error: {err}")
        raise Exception("Database connection failed")

# DB에 URL 존재 여부 및 결과 조회
def check_url_in_db(url):
    query = "SELECT url, is_phishing, total_score FROM url_table WHERE url = %s"
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (url,))
        result = cursor.fetchone()

        if result:
            return {
                "is_phishing": result[1],
                "total_score": result[2],
                "scores": None,
                "results": None
            }
        return None

    except mysql.connector.Error as err:
        logger.error(f"Database query failed: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# URL 검사 결과를 삽입하는 함수
def insert_url_result(url, is_phishing, total_score):
    query = """
        INSERT INTO url_table (url, is_phishing, total_score)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            is_phishing = VALUES(is_phishing),
            total_score = VALUES(total_score)
    """

    values = (url, is_phishing, total_score)

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as err:
        logger.error(f"Failed to insert URL result: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
