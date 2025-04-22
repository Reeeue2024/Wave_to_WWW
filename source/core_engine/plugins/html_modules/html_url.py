# [ URL Modules ] External Resource Analyzer

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract

class HtmlUrl:
    """
    IN : input_url (str)
    OUT : scan 결과 출력 (Phishing 가능성 확률, 탐지 여부)
    """
    def __init__(self, input_url):
        self.input_url = input_url

    def get_registered_domain(self, url: str) -> str:
        ext = tldextract.extract(url)
        return f"{ext.domain}.{ext.suffix}"

    def is_external_resource(self, base_url: str, resource_url: str) -> bool:
        base_domain = self.get_registered_domain(base_url)
        resource_domain = self.get_registered_domain(resource_url)
        return base_domain != resource_domain

    """
    IN : self.input_url
    OUT : 화면 출력 (외부 리소스 비율, 피싱 여부)
    """
    def scan(self):
        print("📦 External Resource Analyzer Module Start.\n")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(self.input_url, headers=headers, timeout=5, allow_redirects=True)
            response.raise_for_status()
            html = response.text
        except requests.exceptions.RequestException as e:
            print(f"[❌] URL 요청 실패: {str(e)}")
            sys.exit(1)

        soup = BeautifulSoup(html, 'html.parser')
        base_url = self.input_url

        resources = []

        # 리소스 추출
        for tag in soup.find_all('link', href=True):
            resources.append(tag['href'])
        for tag in soup.find_all('script', src=True):
            resources.append(tag['src'])
        for tag in soup.find_all('img', src=True):
            resources.append(tag['src'])

        print(f"🔍 총 리소스 수집 개수: {len(resources)}")

        if not resources:
            print("\n✅ 리소스가 없어 피싱 가능성 낮음 (0%)")
            return

        # 외부 리소스 탐지
        external_count = sum(
            self.is_external_resource(base_url, r) or r.startswith('http://')
            for r in resources
        )

        ratio = external_count / len(resources)
        probability = round(ratio * 100, 2)
        is_phishing = probability > 50.0

        print(f"🚨 외부 리소스 비율: {external_count}/{len(resources)}")
        print(f"\n📊 피싱 가능성: {probability}%")
        print(f"🔐 최종 판단: {'Phishing O (위험)' if is_phishing else 'Phishing X (안전)'}")
        print("\n✅ Module End.")

# Module Main
if __name__ == "__main__":
    # Input : URL
    if len(sys.argv) != 2:
        print("사용법: python3 external_resource_analyzer.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    module = HtmlUrl(input_url)
    module.scan()
