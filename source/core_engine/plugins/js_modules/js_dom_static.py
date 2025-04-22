#[ JS Modules ] js_dom_static.py

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

class JsDomStatic:
    """
    IN  : URL
    OUT : 탐지 결과
    """
    def __init__(self, url):
        """
        초기화 및 탐지규칙 설정
        """
        self.url = url
        self.logs = []
        self.score = 0
        self.status = "안전"
        self.rules = [
            {
                "name": "password_input",
                "pattern": r'<input[^>]*type=["\']password["\']',
                "score": 10,
                "message": "비밀번호 입력창 존재 감지"
            },
            {
                "name": "hidden_iframe",
                "pattern": r'<iframe[^>]*(display:\s*none|visibility:\s*hidden|width=["\']?0["\']?|height=["\']?0["\']?)',
                "score": 10,
                "message": "숨겨진 iframe 감지"
            },
            {
                "name": "external_script",
                "pattern": r'<script[^>]+src=["\'](http|https)://(?!.*' + re.escape(urlparse(self.url).netloc) + r')',
                "score": 10,
                "message": "외부 스크립트 삽입 감지"
            },
            {
                "name": "external_form_action",
                "pattern": r'<form[^>]+action=["\'](http|https)://(?!.*' + re.escape(urlparse(self.url).netloc) + r')',
                "score": 10,
                "message": "form 액션이 외부 도메인으로 지정됨"
            },
            {
                "name": "insecure_login_form",
                "pattern": r'<form[^>]+action=["\']http://[^>]*>.*?<input[^>]*type=["\']password["\']',
                "score": 10,
                "message": "비밀번호 전송에 HTTPS 미사용"
            },
            {
                "name": "suspicious_onclick",
                "pattern": r'onclick\s*=\s*["\'].*(document\.location|window\.location|location\.href).*["\']',
                "score": 10,
                "message": "onclick 속성 내 의심스러운 리디렉션 감지"
            },
            {
                "name": "javascript_uri",
                "pattern": r'href\s*=\s*["\']javascript:',
                "score": 10,
                "message": "href 속성에 javascript URI 사용 감지"
            },
            {
                "name": "invisible_link",
                "pattern": r'<a[^>]*(display:\s*none|visibility:\s*hidden|width=["\']?0["\']?|height=["\']?0["\']?)',
                "score": 10,
                "message": "숨겨진 링크 요소 감지"
            },
            {
                "name": "iframe_redirect",
                "pattern": r'<iframe[^>]+src=["\'](http|https)://(?!.*' + re.escape(urlparse(self.url).netloc) + r')',
                "score": 10,
                "message": "외부 도메인으로 연결된 iframe 감지"
            },
            {
                "name": "meta_refresh_redirect",
                "pattern": r'<meta[^>]+http-equiv=["\']refresh["\'][^>]+content=["\']\d+;\s*url=',
                "score": 10,
                "message": "meta refresh 태그를 통한 리디렉션 감지"
            }
        ]

    def run(self):
        """
        IN  : self.url
        OUT : {
            module: 모듈 이름,
            score : 총 탐지 점수,
            status: 안전 / 주의 / 위험,
            logs  : 탐지 로그 리스트
            }
        """
        try:
            response = requests.get(self.url, timeout=5)
            html = response.text
        except Exception as e:
            self.logs.append(f"[접속 실패] {self.url} → {str(e)} (+10점)")
            self.score += 20
            self.status = "주의"
            return self.result()

        soup = BeautifulSoup(html, "html.parser")
        dom = str(soup)

        for rule in self.rules:
            if re.search(rule["pattern"], dom, re.IGNORECASE | re.DOTALL):
                self.logs.append(f"{rule['message']} (+{rule['score']}점)")
                self.score += rule["score"]

        if self.score >= 50:
            self.status = "위험"
        elif self.score >= 20:
            self.status = "주의"
        else:
            self.status = "안전"

        return self.result()

    def result(self):
        return {
            "module": "js_dom_static",
            "score": self.score,
            "status": self.status,
            "logs": self.logs
        }

    def scan(self):
        result = self.run()
        # for log in result["logs"]:
        #     print("[ 탐지 로그 ]", log)
        # print(f"[ 탐지 결과 ] 총점: {result['score']}점")
        # print(f"[ 탐지 결과 ] 위험도: {result['status']}")
        return result["status"] != "안전"
