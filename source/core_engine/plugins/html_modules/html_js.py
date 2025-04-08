# [ URL Modules ] JS Event-Based External Request Analyzer

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
import re

class JsEventAnalyzer:
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

    def extract_urls_from_js(self, js_code: str) -> list[str]:
        # JS 코드에서 외부 URL 추출 (fetch, xhr, etc.)
        pattern = r"""['"]((http|https)://[a-zA-Z0-9\-._~:/?#@!$&'()*+,;=%]+)['"]"""
        return [match[0] for match in re.findall(pattern, js_code)]

    """
    IN : self.input_url
    OUT : 화면 출력 (JS 이벤트 기반 외부 요청 탐지 결과, 피싱 확률)
    """
    def scan(self):
        print("📦 JS Event-Based External Request Analyzer Module Start.\n")

        headers = {
            "User-Agent": "Mozilla/5.0"
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

        event_attrs = ['onclick', 'onmouseover', 'onload', 'onfocus']
        elements_with_events = []

        for attr in event_attrs:
            elements_with_events.extend(soup.find_all(attrs={attr: True}))

        print(f"🔍 이벤트 핸들러 포함 요소 수: {len(elements_with_events)}")

        if not elements_with_events:
            print("\n✅ 이벤트 요소가 없어 피싱 가능성 낮음 (0%)")
            return

        risky_count = 0

        for el in elements_with_events:
            for attr in event_attrs:
                js_code = el.get(attr, '')
                if not js_code:
                    continue

                urls = self.extract_urls_from_js(js_code)
                for url in urls:
                    if self.is_external_domain(base_url, url):
                        risky_count += 1
                        print(f"⚠️ 외부 요청 감지: {url}")
                        break  # 해당 요소는 한 번만 카운트

        ratio = risky_count / len(elements_with_events)
        probability = round(ratio * 100, 2)
        is_phishing = probability > 50.0

        print(f"🚨 의심 이벤트 수: {risky_count}/{len(elements_with_events)}")
        print(f"\n📊 피싱 가능성: {probability}%")
        print(f"🔐 최종 판단: {'Phishing O (위험)' if is_phishing else 'Phishing X (안전)'}")
        print("\n✅ Module End.")

# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 js_event_analyzer.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    module = JsEventAnalyzer(input_url)
    module.scan()
