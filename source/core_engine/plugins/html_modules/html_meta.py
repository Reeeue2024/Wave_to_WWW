# [ URL Modules ] Meta Refresh Redirect Analyzer (Improved + Timing Weight)

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract
import re

class HtmlMeta:
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
        match = re.search(r'url\s*=\s*[\'"]?([^\'";\s]+)', content_value, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def extract_redirect_delay(self, content_value: str) -> float:
        try:
            delay_part = content_value.split(';')[0]
            delay = float(delay_part.strip())
            return delay
        except:
            return 999.0  # 오류 시 매우 큰 값 반환 (무시되도록)

    def scan(self):
        ##print("📦 Meta Refresh Redirect Analyzer (Timing Enhanced) Module Start.\n")

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

        meta_tags = soup.find_all('meta', attrs={'http-equiv': lambda x: x and x.lower() == 'refresh'})
        ##print(f"🔍 meta refresh 태그 개수: {len(meta_tags)}")

        if not meta_tags:
            ##print("\n✅ 리다이렉션 없음 → 피싱 가능성 낮음 (0%)")
            return False

        suspicious_score = 0.0
        checked_tags = 0

        for tag in meta_tags:
            content = tag.get('content', '')
            redirect_url = self.extract_redirect_url(content)
            delay = self.extract_redirect_delay(content)

            if delay > 5:
                continue  # 긴 리디렉션은 무시

            if redirect_url:
                ##print(f"🔗 리다이렉션 URL 발견: {redirect_url} (지연: {delay:.1f}s)")

                if self.is_external_domain(base_url, redirect_url):
                    if delay <= 2:
                        suspicious_score += 1.0
                        ##print("⚠️ 즉시 리디렉션 (0~2초) → 위험도 높음")
                    elif delay <= 5:
                        suspicious_score += 0.5
                        ##print("⚠️ 약간의 리디렉션 지연 (3~5초) → 위험도 보통")

                    checked_tags += 1

        if checked_tags == 0:
            ##print("\n✅ 위험한 리디렉션 없음 (0%)")
            return False

        probability = round((suspicious_score / checked_tags) * 100, 2)
        is_phishing = probability > 10.0

        ##print(f"\n🚨 위험 리디렉션 평균 점수: {suspicious_score}/{checked_tags}")
        ##print(f"📊 피싱 가능성: {probability}%")
        ##print(f"🔐 최종 판단: {'Phishing O (위험)' if is_phishing else 'Phishing X (안전)'}")
        ##print("\n✅ Module End.")
        if is_phishing: return True 
        else: return False

# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        ##print("사용법: python3 meta_redirect_analyzer.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    module = HtmlMeta(input_url)
    module.scan()
