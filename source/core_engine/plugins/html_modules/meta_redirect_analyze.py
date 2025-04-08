# [ URL Modules ] Meta Refresh Redirect Analyzer (Improved)

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract
import re

class MetaRedirectAnalyzer:
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
        target_url_full = urljoin(base_url, target_url)  # 상대경로 처리
        target_domain = self.get_registered_domain(target_url_full)
        return base_domain != target_domain

    def extract_redirect_url(self, content_value: str) -> str | None:
        # 유연한 정규표현식: 공백/따옴표/상대경로 처리
        match = re.search(r'url\s*=\s*[\'"]?([^\'";\s]+)', content_value, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    """
    IN : self.input_url
    OUT : 화면 출력 (meta refresh 탐지 결과, 피싱 확률)
    """
    def scan(self):
        print("📦 Meta Refresh Redirect Analyzer (Improved) Module Start.\n")

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

        meta_tags = soup.find_all('meta', attrs={'http-equiv': lambda x: x and x.lower() == 'refresh'})
        print(f"🔍 meta refresh 태그 개수: {len(meta_tags)}")

        if not meta_tags:
            print("\n✅ 리다이렉션 없음 → 피싱 가능성 낮음 (0%)")
            return

        suspicious_count = 0

        for tag in meta_tags:
            content = tag.get('content', '')
            redirect_url = self.extract_redirect_url(content)

            if redirect_url:
                print(f"🔗 리다이렉션 URL 발견: {redirect_url}")
                if self.is_external_domain(base_url, redirect_url):
                    suspicious_count += 1

        ratio = suspicious_count / len(meta_tags)
        probability = round(ratio * 100, 2)
        is_phishing = probability > 50.0

        print(f"🚨 의심 리다이렉션 비율: {suspicious_count}/{len(meta_tags)}")
        print(f"\n📊 피싱 가능성: {probability}%")
        print(f"🔐 최종 판단: {'Phishing O (위험)' if is_phishing else 'Phishing X (안전)'}")
        print("\n✅ Module End.")

# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 meta_redirect_analyzer.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    module = MetaRedirectAnalyzer(input_url)
    module.scan()
