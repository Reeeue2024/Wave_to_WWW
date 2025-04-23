# [ JS Modules ] External Server Static

import sys
import requests
import re

class JsExfilStatic:
    """
    IN : URL (string to raw JS file)
    OUT : score (float) : 0.0 ~ 1.0
    """

    def __init__(self, input_url):
        self.input_url = input_url

    def scan(self):
        # print("Module Start: [JS External Server Static]")

        try:
            response = requests.get(self.input_url)
            response.raise_for_status()
            js_code = response.text

            # 외부 서버로 정보 전송하는 패턴
            patterns = [
                r"fetch\s*\(\s*['\"]http[s]?://[^'\"]*steal[^'\"]*['\"]",       # fetch('http://.../steal...')
                r"fetch\s*\(\s*['\"]http[s]?://[^'\"]*malicious[^'\"]*['\"]",   # fetch('http://malicious...')
                r"\.addEventListener\s*\(\s*['\"]submit['\"]",                  # form submit 이벤트 감지
                r"\.addEventListener\s*\(\s*['\"]key(down|up)['\"]",            # 키 입력 감지 이벤트
                r"new\s+FormData\s*\(",                                         # FormData 객체 사용
                r"new\s+URLSearchParams\s*\(",                                  # URLSearchParams 사용
                r"\.preventDefault\s*\(\s*\)",                                  # 기본 전송 방지
            ]

            suspicious_hits = []

            for pattern in patterns:
                matches = re.findall(pattern, js_code)
                if matches:
                    suspicious_hits.extend(matches)

            if suspicious_hits:
                # print(f"[Detected] JS Exfil : {suspicious_hits}")
                # print("→ Score: 1.0 (0.0: Safe, 1.0: High Risk)")
                # print("\nModule End.")
                return True
            else:
                # print(f"[Normal] No JS EXfil: {self.input_url}")
                # print("→ Score: 0.0 (0.0: Safe, 1.0: High Risk)")
                # print("\nModule End.")
                return False

        except requests.RequestException as e:
            # print(f"[ERROR] Failed to fetch JS file: {e}")
            # print("→ Score: 0.0 (0.0: Safe, 1.0: High Risk)")
            # print("\nModule End.")
            return False


# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("How to Use : python3 js_exfil_static.py <JS URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    exfil_detector = JsExfilStatic(input_url)
    exfil_detector.scan()