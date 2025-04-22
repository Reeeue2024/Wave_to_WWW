# [ JS Modules ] js_script_static.py

import requests
from bs4 import BeautifulSoup
import re

class JsScriptStatic:
    """
    IN  : URL
    OUT : 탐지 결과
    """
    def __init__(self, url):
        """
        초기화 및 탐지규칙 설정
        """
        self.url = url
        self.score = 0
        self.logs = []
        self.status = "안전"
        self.rules = [
            {
                "name": "suspiciousCdn",
                "pattern": r"https?://[^\s'\"]*(?:malicious|track|spy|steal|adserver)[^\s'\"]*",
                "score": 10,
                "message": "의심스럽고 복잡한 CDN URL 검지"
            },
            {
                "name": "inlineEventScript",
                "pattern": r"<script[^>]*>.*(onerror|onload|onclick)=.*</script>",
                "score": 10,
                "message": "inline event 기능의 스크립트 검지"
            },
            {
                "name": "dataJsUrl",
                "pattern": r"data:text/javascript",
                "score": 10,
                "message": "data URI 구조의 스크립트 삽입 검지"
            },
            {
                "name": "documentWrite",
                "pattern": r"document\.write(ln)?\s*\(",
                "score": 10,
                "message": "document.write 사용 감지"
            },
            {
                "name": "suspiciousKeyword",
                "pattern": r"(steal|track|keylog|cookie|grab)[a-z]*\b",
                "score": 10,
                "message": "의심 키워드 포함 스크립트 감지"
            },
            {
                "name": "base64EncodedString",
                "pattern": r"atob\s*\(|btoa\s*\(|[A-Za-z0-9+/]{50,}={0,2}",
                "score": 10,
                "message": "Base64 디코딩 또는 인코딩 스크립트 감지"
            },
            {
                "name": "script_in_img_tag",
                "pattern": r"<img[^>]+src=['\"]javascript:",
                "score": 10,
                "message": "<img> 태그에서 javascript: 사용 감지"
            },
            {
                "name": "script_src_inline_mix",
                "pattern": r"<script[^>]+src=.*?>.*?</script>",
                "score": 10,
                "message": "<script> 태그에서 src와 inline 코드 병용 감지"
            },
            {
                "name": "iframe_javascript_src",
                "pattern": r"<iframe[^>]+src=['\"]javascript:",
                "score": 10,
                "message": "<iframe>의 src 속성에 javascript URI 사용 감지"
            },
            {
                "name": "cookie_access",
                "pattern": r"document\.cookie",
                "score": 10,
                "message": "document.cookie 접근 코드 감지"
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
            self.logs.append(f"[접속 실패] (+20점) {self.url} → {str(e)}")
            self.score += 20
            self.status = "주의"
            return self.result()

        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")
        full_script_html = "\n".join(str(script) for script in scripts)

        for rule in self.rules:
            if re.search(rule["pattern"], full_script_html, re.IGNORECASE):
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
            "module": "Script Injection Detector (Static - BS)",
            "score": self.score,
            "status": self.status,
            "logs": self.logs
        }

    def scan(self):
        result = self.run()
        for log in result["logs"]:
            print("[ 탐지 로그 ]", log)
        print(f"[ 탐지 결과 ] 총점: {result['score']}점")
        print(f"[ 탐지 결과 ] 위험도: {result['status']}")
        return result["status"] != "안전"
