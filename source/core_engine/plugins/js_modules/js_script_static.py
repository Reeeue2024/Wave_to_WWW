#[ JS Modules ] script_injection_detector_static.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
        self.driver = None

        self.detection_rules = [
            {
                "name": "suspiciousCdn",
                "pattern": r"https?://[^\s'\"]*(malicious|track|spy|steal|adserver)[^\s'\"]*",
                "score": 25,
                "message": "의심스럽고 복잡한 CDN URL 검지",
                "detected": False
            },
            {
                "name": "inlineEventScript",
                "pattern": r"<script[^>]*>.*(onerror|onload|onclick)=.*</script>",
                "score": 15,
                "message": "inline event 기능의 스크립트 검지",
                "detected": False
            },
            {
                "name": "dataJsUrl",
                "pattern": r"data:text/javascript",
                "score": 20,
                "message": "data URI 구조의 스크립트 삽입 검지",
                "detected": False
            },
            {
                "name": "documentWrite",
                "pattern": r"document\.write(ln)?\s*\(",
                "score": 15,
                "message": "document.write 사용 감지",
                "detected": False
            },
            {
                "name": "suspiciousKeyword",
                "pattern": r"(steal|track|keylog|cookie|grab)[a-z]*\b",
                "score": 15,
                "message": "의심 키워드 포함 스크립트 감지",
                "detected": False
            },
            {
                "name": "base64EncodedString",
                "pattern": r"atob\s*\(|btoa\s*\(|[A-Za-z0-9+/]{50,}={0,2}",
                "score": 10,
                "message": "Base64 디코딩 또는 인코딩 스크립트 감지",
                "detected": False
            }
        ]

    def setup_driver(self):
        """
        headless Chrome 드라이버 설정
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(5)

    def run(self):
        """
        IN  : self.url
        OUT : {
            module: 모듈 이름,
            score : 총 탐지 점수,
            status: 안전 / 주의 / 위험,
            logs  : 탐지 로그 리스트
        }
        - 브라우저 통해 접속 시도, 접속 실패하는 경우도 "주의"로 판단
        - 렌더링 <script> 태그의 전체 HTML(outerHTML) 기반으로 탐지 수행
        """
        self.setup_driver()

        try:
            self.driver.get(self.url)
        except Exception as e:
            self.logs.append(f"[접속 실패] (+20점) {self.url} → {str(e)}")
            self.score += 20
            self.status = "주의"
            self.driver.quit()
            return {
                "module": "Script Injection Detector (Static)",
                "score": self.score,
                "status": self.status,
                "logs": self.logs
            }

        scripts = self.driver.find_elements("tag name", "script")

        content = ""
        for script in scripts:
            content += script.get_attribute("outerHTML") or ""

            for rule in self.detection_rules:
                if not rule["detected"] and re.search(rule["pattern"], content):
                    message = f"{rule['message']} (+{rule['score']}점)"
                    self.logs.append(message)
                    self.score += rule["score"]
                    rule["detected"] = True

        # 위험도 계산
        if self.score >= 50:
            self.status = "위험"
        elif self.score >= 20:
            self.status = "주의"
        else:
            self.status = "안전"

        self.driver.quit()

        return {
            "module": "Script Injection Detector (Static)",
            "score": self.score,
            "status": self.status,
            "logs": self.logs
        }

    def scan(self):
        """
        - run() 실행 결과를 바탕으로 로그와 위험도 출력
        - 최종 위험도에 따라 Boolean 결과 반환
        """
        result = self.run()
        for log in result["logs"]:
            print("[ 탐지 로그 ]", log)
        print(f"[ 탐지 결과 ] 총점: {result['score']}점")
        print(f"[ 탐지 결과 ] 위험도: {result['status']}")
        return result["status"] != "안전"
