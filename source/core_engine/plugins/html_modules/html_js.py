# [ URL Modules ] JS Event-Based External Request Analyzer (Upgraded with <script> analysis)

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
import re

class HtmlJs:
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
        pattern = r"""['"]((http|https)://[a-zA-Z0-9\-._~:/?#@!$&'()*+,;=%]+)['"]"""
        return [match[0] for match in re.findall(pattern, js_code)]

    def scan(self):
        ##print("📦 JS Event-Based External Request Analyzer (Enhanced) Module Start.\n")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(self.input_url, headers=headers, timeout=5)
            response.raise_for_status()
            html = response.text
        except requests.exceptions.RequestException as e:
            ##print(f"[❌] URL 요청 실패: {str(e)}")
            return False


        soup = BeautifulSoup(html, 'html.parser')
        base_url = self.input_url

        event_attrs = ['onclick', 'onmouseover', 'onload', 'onfocus']
        elements_with_events = []

        for attr in event_attrs:
            elements_with_events.extend(soup.find_all(attrs={attr: True}))

        ##print(f"🔍 이벤트 핸들러 포함 요소 수: {len(elements_with_events)}")

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
                        ##print(f"⚠️ [이벤트] 외부 요청 감지: {url}")
                        break

        # ➕ <script> 태그 내부의 JS 코드도 분석
        script_tags = soup.find_all("script")
        ##print(f"\n🧠 <script> 태그 개수: {len(script_tags)}")

        script_risky_count = 0

        for script in script_tags:
            if script.string:
                js_code = script.string
                urls = self.extract_urls_from_js(js_code)
                for url in urls:
                    if self.is_external_domain(base_url, url):
                        script_risky_count += 1
                        ##print(f"⚠️ [스크립트] 외부 요청 감지: {url}")
                        break  # 하나만 감지해도 해당 <script>는 의심 처리

        total_risky = risky_count + script_risky_count
        total_elements = len(elements_with_events) + len(script_tags)
        if total_elements == 0:
            ##print("\n✅ JS 이벤트와 <script> 요소가 없어 피싱 가능성 낮음 (0%)")
            return False

        ratio = total_risky / total_elements
        probability = round(ratio * 100, 2)
        is_phishing = probability > 20.0

        ##print(f"\n🚨 의심 JS 요소 수: {total_risky}/{total_elements}")
        ##print(f"📊 피싱 가능성: {probability}%")
        ##print(f"🔐 최종 판단: {'Phishing O (위험)' if is_phishing else 'Phishing X (안전)'}")
        ##print("\n✅ Module End.")
        if total_risky: return True 
        else: return False


# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        ##print("사용법: python3 js_event_analyzer.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    module = HtmlJs(input_url)
    module.scan()
