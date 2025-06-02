# [ Server ] kisa_report.py
# source/server/app/utils/kisa_report.py

import smtplib
from email.mime.text import MIMEText
from email.header import Header
# from dotenv import load_dotenv
from datetime import datetime
from .logger import logger
import os

# load_dotenv(dotenv_path="../.env")

# KISA 리포트용 이메일
KISA_REPORT_EMAIL = "phishingreport423@gmail.com"  # 테스트용 메일
# KISA_REPORT_EMAIL = "phishing@boho.or.kr"  # 실제 리포트용 메일

# 발신자 이메일 및 SMTP 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# 환경 변수 누락 시 예외 처리
if not SMTP_USER or not SMTP_PASSWORD:
    raise EnvironmentError("[SMTP 설정 오류] SMTP_USER 또는 SMTP_PASSWORD 환경변수가 누락되었습니다.")

# 탐지 결과 리스트 HTML 테이블 형식으로 변환
def format_module_results_to_html(modules: list[dict]) -> str:
    rows = ""
    for module in modules:
        name = module.get("module_class_name")
        result = "위험" if module.get("module_result_flag") else "정상"
        evidence_data = module.get("module_result_data")
        if isinstance(evidence_data, dict):
            evidence = evidence_data.get("evidence", str(evidence_data))
        else:
            evidence = str(evidence_data) if evidence_data is not None else "x"

        if name is None or result is None:
            continue

        rows += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ccc; white-space: nowrap;">{name}</td>
            <td style="padding: 8px; border: 1px solid #ccc; white-space: nowrap; ">{result}</td>
            <td style="padding: 8px; border: 1px solid #ccc;">{evidence}</td>
        </tr>"""
    table = f"""
    <table style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
        <thead>
            <tr>
                <th style="padding: 8px; border: 1px solid #ccc; background-color: #f2f2f2;">모듈 이름</th>
                <th style="padding: 8px; border: 1px solid #ccc; background-color: #f2f2f2;">탐지 결과</th>
                <th style="padding: 8px; border: 1px solid #ccc; background-color: #f2f2f2;">근거</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>"""
    return table

# 자동 리포트 이메일 전송
def report_to_kisa(url: str, score: float = 0.0, modules: list[dict] = []) -> bool:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    module_table = format_module_results_to_html(modules)

    html_body = f"""
    <html>
    <body>
        <p>안녕하세요. 피싱 탐지 시스템 <strong>'wave to www'</strong>입니다.</p>

        <p>아래 URL이 피싱 사이트로 탐지되어 자동 신고 메일을 발송합니다:</p>
        <ul>
            <li><strong>URL:</strong> {url}</li>
            <li><strong>탐지 점수:</strong> {score}</li>
            <li><strong>탐지 일시:</strong> {timestamp}</li>
        </ul>

        <p><strong>근거 자료: 탐지 시스템의 모듈별 탐지 결과</strong></p>
        {module_table}

        <p style="margin-top: 20px;">본 메일은 비영리 프로젝트의 자동화된 시스템에 의해 발송되었습니다.<br>감사합니다.</p>
    </body>
    </html>
    """
    
    # 메일 헤더 및 MIME 설정
    msg = MIMEText(html_body, "html", "utf-8")
    msg["Subject"] = Header("피싱 URL 자동 제보", "utf-8")
    msg["From"] = SMTP_USER
    msg["To"] = KISA_REPORT_EMAIL

    try:
        # SMTP 서버 접속, 메일 전송
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [KISA_REPORT_EMAIL], msg.as_string())
        logger.info(f"[KISA Report] URL reported successfully: {url}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"[SMTP 인증 오류] 로그인 실패 - 계정 또는 비밀번호 오류: {e}")
    except smtplib.SMTPConnectError as e:
        logger.error(f"[SMTP 연결 오류] 서버 연결 실패: {e}")
    except smtplib.SMTPRecipientsRefused as e:
        logger.error(f"[SMTP 수신자 오류] 수신자 주소 거부됨: {e.recipients}")
    except smtplib.SMTPDataError as e:
        logger.error(f"[SMTP 데이터 오류] 전송 데이터 문제: {e}")
    except smtplib.SMTPException as e:
        logger.error(f"[SMTP 일반 오류] SMTP 전송 중 예외 발생: {e}")
    except Exception as e:
        logger.error(f"[SMTP 처리 실패] 알 수 없는 오류 발생: {type(e).__name__} | {e}")
    
    return False


# 단독 실행 시 테스트 코드
"""
if __name__ == "__main__":
    dummy_url = "http://phishing-example.test"
    dummy_score = 92.3
    dummy_modules = [
        {"module_name": "BlacklistCheck", "result_flag": True, "module_score": 95},
        {"module_name": "MLDetection", "result_flag": False, "module_score": 70},
        {"module_name": "HeuristicAnalysis", "result_flag": True, "module_score": 90}
    ]

    success = report_to_kisa(dummy_url, dummy_score, dummy_modules)
    print("메일 발송 성공" if success else "메일 발송 실패")
"""
