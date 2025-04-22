# [ URL Modules ] Iframe Overlay Analyzer

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract

class HtmlIframe:
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
    OUT : 화면 출력 (iframe + 가짜 로그인 탐지 결과, 피싱 확률)
    """
    def scan(self):
        print("📦 Iframe Overlay Analyzer Module Start.\n")

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

        iframes = soup.find_all('iframe', src=True)
        print(f"🔍 iframe 태그 개수: {len(iframes)}")

        if not iframes:
            print("\n✅ iframe이 없어 피싱 가능성 낮음 (0%)")
            return

        suspicious_count = 0

        for iframe in iframes:
            src = iframe['src']
            if self.is_external_domain(base_url, src):
                suspicious_count += 1

        # 위장 로그인 시도 탐지
        fake_login = soup.find('input', {'type': 'password'})
        high_zindex_elements = soup.find_all(style=True)
        high_zindex_found = False

        for el in high_zindex_elements:
            style = el['style']
            if 'z-index' in style:
                try:
                    z = int(style.split('z-index:')[-1].split(';')[0].strip())
                    if z >= 100:
                        high_zindex_found = True
                        break
                except:
                    continue

        if fake_login and high_zindex_found:
            suspicious_count += 1
            print("⚠️ 위장 로그인 시도 감지됨 (패스워드 + 높은 z-index)")

        total_check = len(iframes) + 1  # +1: 위장 로그인 여부 포함
        ratio = suspicious_count / total_check
        probability = round(ratio * 100, 2)
        is_phishing = probability > 50.0

        print(f"🚨 의심 요소 개수: {suspicious_count}/{total_check}")
        print(f"\n📊 피싱 가능성: {probability}%")
        print(f"🔐 최종 판단: {'Phishing O (위험)' if is_phishing else 'Phishing X (안전)'}")
        print("\n✅ Module End.")

# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 iframe_overlay_analyzer.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    module = HtmlIframe(input_url)
    module.scan()
