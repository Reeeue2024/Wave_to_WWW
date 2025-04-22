# [ URL Modules ] Form Action Analyzer

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract

class HtmlForm:
    """
    IN : input_url (str)
    OUT : scan 결과 출력 (Phishing 가능성 확률, 탐지 여부)
    """
    def __init__(self, input_url):
        self.input_url = input_url

    def get_registered_domain(self, url: str) -> str:
        ext = tldextract.extract(url)
        return f"{ext.domain}.{ext.suffix}"

    def is_external_domain(self, base_url: str, target_url: str) -> bool:
        base_domain = self.get_registered_domain(base_url)
        target_domain = self.get_registered_domain(target_url)
        return base_domain != target_domain

    """
    IN : self.input_url
    OUT : 화면 출력 (form action 분석 결과, 피싱 확률)
    """
    def scan(self):
        print("📦 Form Action Analyzer Module Start.\n")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(self.input_url, headers=headers, timeout=5)
            response.raise_for_status()
            html = response.text
        except requests.exceptions.RequestException as e:
            print(f"[❌] URL 요청 실패: {str(e)}")
            sys.exit(1)

        soup = BeautifulSoup(html, 'html.parser')
        base_url = self.input_url
        forms = soup.find_all('form')

        print(f"🔍 form 태그 개수: {len(forms)}")

        if not forms:
            print("\n✅ form이 없어 피싱 가능성 낮음 (0%)")
            return

        risky_forms = 0

        for form in forms:
            action = form.get('action', '')
            has_password = bool(form.find('input', {'type': 'password'}))

            # 외부 도메인으로 데이터를 보내는 경우
            if self.is_external_domain(base_url, action):
                risky_forms += 1

            # 비밀번호 입력 필드가 있으나 HTTPS가 아닐 때
            if has_password and not base_url.startswith('https://'):
                risky_forms += 1

        ratio = risky_forms / len(forms)
        probability = round(ratio * 100, 2)
        is_phishing = probability > 50.0

        print(f"🚨 위험한 form 비율: {risky_forms}/{len(forms)}")
        print(f"\n📊 피싱 가능성: {probability}%")
        print(f"🔐 최종 판단: {'Phishing O (위험)' if is_phishing else 'Phishing X (안전)'}")
        print("\n✅ Module End.")

# Module Main
if __name__ == "__main__":
    # Input : URL
    if len(sys.argv) != 2:
        print("사용법: python3 form_action_analyzer.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    module = HtmlForm(input_url)
    module.scan()
