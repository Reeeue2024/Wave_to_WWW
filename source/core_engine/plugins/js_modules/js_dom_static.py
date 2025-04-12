# [ JS Modules ] obfuscation_detector_static

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time

class JsObfuscationStatic:
    """
    IN  : URL
    OUT : 탐지 결과
    """

    def __init__(self, url):
        self.url = url
        self.score = 0
        self.logs = []
        self.status = "안전"
        self.driver = None

        # 탐지 규칙 정의
        self.detection_rules = [
            {
                "name": "password_input",
                "check": self.detect_password_input,
                "score": 15,
                "message": "비밀번호 입력창 존재 감지"
            },
            {
                "name": "hidden_iframe",
                "check": self.detect_hidden_iframe,
                "score": 15,
                "message": "숨겨진 iframe 감지"
            },
            {
                "name": "external_script",
                "check": self.detect_external_script,
                "score": 20,
                "message": "외부 스크립트 삽입 감지"
            },
            {
                "name": "external_form_action",
                "check": self.detect_external_form_action,
                "score": 25,
                "message": "form 액션이 외부 도메인으로 지정됨"
            },
            {
                "name": "insecure_login_form",
                "check": self.detect_insecure_login_form,
                "score": 25,
                "message": "비밀번호 전송에 HTTPS 미사용"
            }
        ]

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(5)

    def run(self):
        self.setup_driver()

        try:
            self.driver.get(self.url)
            time.sleep(1)  # JS 렌더링 대기
        except Exception as e:
            self.logs.append(f"[접속 실패] (+10점) {self.url} → {str(e)}")
            self.score += 10
            self.status = "주의"
            self.driver.quit()
            return self.result()

        for rule in self.detection_rules:
            if rule["check"]():
                self.logs.append(f"{rule['message']} (+{rule['score']}점)")
                self.score += rule["score"]

        self.driver.quit()
        self.status = self.determine_status()
        return self.result()

    def detect_password_input(self):
        return bool(self.driver.find_elements("xpath", "//input[@type='password']"))

    def detect_hidden_iframe(self):
        iframes = self.driver.find_elements("tag name", "iframe")
        for iframe in iframes:
            style = iframe.get_attribute("style") or ""
            width = iframe.get_attribute("width") or ""
            height = iframe.get_attribute("height") or ""
            if "display: none" in style or "visibility: hidden" in style or width == "0" or height == "0":
                return True
        return False

    def detect_external_script(self):
        scripts = self.driver.find_elements("tag name", "script")
        for script in scripts:
            src = script.get_attribute("src")
            if src and not self.url in src and "file://" not in src and "localhost" not in src:
                return True
        return False

    def detect_external_form_action(self):
        forms = self.driver.find_elements("tag name", "form")
        current_domain = urlparse(self.url).netloc
        for form in forms:
            action = form.get_attribute("action") or ""
            if action.startswith("http"):
                action_domain = urlparse(action).netloc
                if current_domain not in action_domain:
                    return True
        return False

    def detect_insecure_login_form(self):
        forms = self.driver.find_elements("tag name", "form")
        for form in forms:
            password_inputs = form.find_elements("xpath", ".//input[@type='password']")
            if password_inputs:
                action = form.get_attribute("action") or ""
                if action.startswith("http://") or (action.startswith("http") and not action.startswith("https://")):
                    return True
        return False

    def determine_status(self):
        if self.score >= 50:
            return "위험"
        elif self.score >= 20:
            return "주의"
        return "안전"

    def result(self):
        return {
            "module": "DOM Change Detector (Static)",
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
