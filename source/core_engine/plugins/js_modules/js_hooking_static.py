# [ JS Modules ] Hooking Static

import os
import sys
import requests
from bs4 import BeautifulSoup
import re
import urllib3

# InsecureRequestWarning 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class JsHookingStatic:
    """
    IN  : URL (str)
    OUT : score (float) : 0.0 ~ 1.0
    """
    def __init__(self, input_url):
        self.input_url = input_url

    # 후킹 패턴 정의 및 점수 부여
    HOOKING_PATTERNS = {
        r'addEventListener': 0.12,  # 이벤트 후킹
        r'onclick': 0.09,            # 클릭 후킹
        r'onkeyup': 0.08,            # 키 입력 후킹
        r'onkeydown': 0.08,          # 키 입력 후킹
        r'MutationObserver': 0.13,   # DOM 변경 후킹
        r'XMLHttpRequest': 0.11,     # XHR 후킹
        r'fetch': 0.11,              # fetch 후킹
        r'eval': 0.16,               # eval 함수 후킹
        r'unescape': 0.11,           # unescape 후킹
        r'atob': 0.11                # Base64 디코딩 후킹
    }

    # 후킹 패턴의 총 점수 합산 (정규화 없이 그대로 합산)
    MAX_SCORE = sum(HOOKING_PATTERNS.values())

    """
    IN : URL
    OUT : Scan Result (True : Phishing O / False : Phishing X)
    """
    def scan(self):
        # print(f"Module Start: [JS Hooking Static]")

        # 웹 페이지 요청 (SSL 인증서 검사를 비활성화)
        response = requests.get(self.input_url, verify=False)  # SSL 인증서 검사를 비활성화
        if response.status_code != 200:
            # print(f"[Error] Failed to retrieve {self.input_url} - Status Code: {response.status_code}")
            return False

        # 파일이 HTML인지, JS 파일인지를 판단
        content_type = response.headers.get('Content-Type', '')
        if 'html' in content_type:  # HTML인 경우
            return self._scan_html(response.text)
        elif 'javascript' in content_type or self.input_url.endswith('.js'):  # JS 파일인 경우
            return self._scan_js(response.text)
        else:
            # print(f"[Error] Unsupported content type: {content_type}")
            return False

    def _scan_html(self, html_content):
        """
        IN : html_content (string) : HTML 페이지의 내용
        OUT : Scan Result (True : Detected / False : No Hooking) 
        - HTML 페이지 내에서 JavaScript 코드 추출 및 후킹 패턴 분석
        """
        # print(f"Scanning HTML content...")

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(html_content, 'html.parser')

        # 모든 JavaScript 코드 추출
        scripts = soup.find_all('script')
        hooking_matches = []
        total_score = 0  # 후킹 점수 합산

        # JavaScript 코드에서 후킹 관련 패턴을 찾음
        for script in scripts:
            if script.string:
                for pattern, score in self.HOOKING_PATTERNS.items():
                    matches = re.findall(pattern, script.string, re.IGNORECASE)
                    if matches:
                        hooking_matches.append({
                            'pattern': pattern,
                            'score': score  # 후킹 패턴의 점수
                        })
                        total_score += score  # 점수 합산

        if hooking_matches:
            patterns_found = [f"{match['pattern']} (+{match['score']})" for match in hooking_matches]
            # print(f"[Detected] JS Hooking: {patterns_found}")
            # print(f"→ Score: {total_score:.2f} (0.0: Safe, 1.0: High Risk)")
            # print(f"\nModule End.")
            return True

        # print(f"[Normal] No JS Hooking: {self.input_url}")
        # print(f"→ Score: {total_score:.2f} (0.0: Safe, 1.0: High Risk)")
        # print(f"\nModule End.")
        return False

    def _scan_js(self, js_content):
        """
        IN : js_content (string) : JavaScript 파일의 내용
        OUT : Scan Result (True : Detected / False : No Hooking)
        - JavaScript 파일에서 후킹 패턴 분석
        """
        # print(f"Scanning JS content...")

        hooking_matches = []
        total_score = 0  # 후킹 점수 합산

        # JavaScript 코드에서 후킹 관련 패턴을 찾음
        for pattern, score in self.HOOKING_PATTERNS.items():
            matches = re.findall(pattern, js_content, re.IGNORECASE)
            if matches:
                hooking_matches.append({
                    'pattern': pattern,
                    'score': score  # 후킹 패턴의 점수
                })
                total_score += score  # 점수 합산

        if hooking_matches:
            patterns_found = [f"{match['pattern']} (+{match['score']})" for match in hooking_matches]
            # print(f"[Detected] JS Hooking: {patterns_found}")
            # print(f"→ Score: {total_score:.2f} (0.0: Safe, 1.0: High Risk)")
            # print(f"\nModule End.")
            return True

        # print(f"[Normal] No JS Hooking: {self.input_url}")
        # print(f"→ Score: {total_score:.2f} (0.0: Safe, 1.0: High Risk)")
        # print(f"\nModule End.")
        return False


# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 js_hooking_static.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    js_hooking_static = JsHookingStatic(input_url)
    js_hooking_static.scan()
