# [ URL Modules ] Iframe Overlay Analyzer (with CSS z-index + display/size/position analysis)

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
import tinycss2  # pip install tinycss2

class HtmlIframe:
    def __init__(self, input_url):
        self.input_url = input_url

    def get_registered_domain(self, url: str) -> str:
        ext = tldextract.extract(url)
        return f"{ext.domain}.{ext.suffix}"

    def is_external_domain(self, base_url: str, target_url: str) -> bool:
        base_domain = self.get_registered_domain(base_url)
        target_domain = self.get_registered_domain(target_url)
        return base_domain != target_domain

    def extract_z_index(self, style_string: str) -> int | None:
        try:
            for rule in style_string.split(';'):
                if 'z-index' in rule:
                    key, value = rule.split(':')
                    if 'z-index' in key.strip().lower():
                        return int(value.strip())
        except:
            pass

        try:
            declarations = tinycss2.parse_declaration_list(style_string)
            for decl in declarations:
                if decl.type == 'declaration' and decl.name == 'z-index' and not decl.invalid:
                    for token in decl.value:
                        if token.type == 'number':
                            return int(token.value)
        except:
            pass

        return None

    def scan(self):
        ##print("📦 Iframe Overlay Analyzer Module Start.\n")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"
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

        iframe_tags = soup.find_all('iframe', src=True)
        object_tags = soup.find_all('object', data=True)
        embed_tags = soup.find_all('embed', src=True)

        suspicious_count = 0

        total_tags = iframe_tags + object_tags + embed_tags
        ##print(f"🔍 포함된 태그 개수 (iframe/object/embed): {len(total_tags)}")

        if not total_tags:
            ##print("\n✅ iframe/object/embed 태그 없음 → 피싱 가능성 낮음 (0%)")
            return False

        for tag in total_tags:
            src_attr = 'src' if tag.name in ['iframe', 'embed'] else 'data'
            src = tag.get(src_attr, '')
            if self.is_external_domain(base_url, src):
                suspicious_count += 1

            style = tag.get('style', '').lower()
            if any(keyword in style for keyword in ['display:none', 'opacity:0', 'visibility:hidden']):
                ##print("⚠️ 숨김 속성 감지됨")
                suspicious_count += 1

            if tag.get('width') == '100%' or tag.get('height') == '100%':
                ##print("⚠️ 화면 전체를 덮는 태그 감지 (width/height=100%)")
                suspicious_count += 1

        fake_login = soup.find('input', {'type': 'password'})
        high_zindex_elements = soup.find_all(style=True)
        high_zindex_found = False

        for el in high_zindex_elements:
            style = el['style']
            z = self.extract_z_index(style)
            if z is not None and z >= 100:
                high_zindex_found = True
                break

        absolute_overlay_found = False
        for div in soup.find_all('div', style=True):
            style = div['style'].lower()
            if 'position:absolute' in style and fake_login:
                absolute_overlay_found = True
                suspicious_count += 1
                ##print("⚠️ 로그인 UI를 덮는 position:absolute div 감지")
                break

        if fake_login and high_zindex_found:
            suspicious_count += 1
            ##print("⚠️ 위장 로그인 시도 감지됨 (패스워드 + 높은 z-index)")

        total_check = len(total_tags) + 3
        ratio = suspicious_count / total_check
        probability = round(ratio * 100, 2)
        is_phishing = probability > 50.0

        ##print(f"🚨 의심 요소 개수: {suspicious_count}/{total_check}")
        ##print(f"\n📊 피싱 가능성: {probability}%")
        ##print(f"🔐 최종 판단: {'Phishing O (위험)' if is_phishing else 'Phishing X (안전)'}")
        ##print("\n✅ Module End.")
        if is_phishing: return True 
        else: return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        ##print("사용법: python3 iframe_overlay_analyzer.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    module = HtmlIframe(input_url)
    module.scan()
