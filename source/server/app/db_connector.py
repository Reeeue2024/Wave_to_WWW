# [ Server ] db_connector.py
# source/server/app/db_connector.py

import mysql.connector
import logging
from dotenv import load_dotenv
import json
import os

# 환경변수 로드
load_dotenv(dotenv_path="server/app/.env")

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

# DB 초기화 (생성)
def initialize_url_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS url_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            input_url VARCHAR(2083) NOT NULL,
            engine_result_flag BOOLEAN NOT NULL,
            engine_result_score INT,
            module_result_dictionary_list JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_input_url (input_url(768))
        )
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        logger.info("url_table created or already exists.")
    except mysql.connector.Error as err:
        logger.error(f"Failed to create url_table: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# DB에 URL 존재 여부 및 결과 조회
def check_url_in_db(url):
    query = """
        SELECT input_url, engine_result_flag, engine_result_score, module_result_dictionary_list
        FROM url_table
        WHERE input_url = %s
    """
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (url,))
        result = cursor.fetchone()

        if result:
            import json
            module_result_dict = json.loads(result[3]) if result[3] else []
            return {
                "input_url": result[0],
                "engine_result_flag": result[1],
                "engine_result_score": result[2],
                "module_result_dictionary_list": module_result_dict
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
def insert_url_result(input_url, engine_result_flag, engine_result_score, module_result_dictionary_list):
    query = """
        INSERT INTO url_table (
            input_url, engine_result_flag, engine_result_score, module_result_dictionary_list
        )
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            engine_result_flag = VALUES(engine_result_flag),
            engine_result_score = VALUES(engine_result_score),
            module_result_dictionary_list = VALUES(module_result_dictionary_list)
    """

    module_json = json.dumps(module_result_dictionary_list, ensure_ascii=False)
    values = (input_url, engine_result_flag, engine_result_score, module_json)

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
