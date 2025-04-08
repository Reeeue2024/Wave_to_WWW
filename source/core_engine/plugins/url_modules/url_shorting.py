# [ URL / Domain Modules ] 단축 URL 사용 여부를 바탕으로 탐지

# 이 모듈은 "리디렉션을 따라가서 최종 URL을 얻는다"까지만 함
# 피싱 판별 등은 다른 모듈로 넘김

import os
import sys
import re
import requests

class ShortenedURLDetector:
    """
    IN : URL (string)
    OUT : 
        - is_shortened (bool) : 단축 URL 여부
        - original_url (string) : 리디렉션된 원본 URL (단축일 경우)
    """
    def __init__(self, input_url):
        self.input_url = input_url
        self.original_url = None

        # 자주 사용되는 단축 URL 도메인 목록
        self.short_url_domains = [
            "bit.ly", "goo.gl", "t.co", "ow.ly", "tinyurl.com",
            "is.gd", "buff.ly", "adf.ly", "bit.do", "mcaf.ee",
            "rebrand.ly", "su.pr", "shorte.st", "cli.gs", "v.gd"
        ]
    
    def is_shortened_url(self):
        """
        단축 URL 여부를 확인하는 함수
        """
        for domain in self.short_url_domains:
            # 입력된 URL이 단축 도메인을 포함하는지 정규표현식으로 검사
            if re.search(rf"https?://(www\.)?{re.escape(domain)}(/|$)", self.input_url):
                return True
        return False

    def expand_url(self):
        """
        단축 URL인 경우 리디렉션을 따라가 최종 목적지 URL을 찾는 함수
        """
        try:
            # HEAD 요청을 보내 리디렉션 확인 (파일 다운로드 없음)
            response = requests.head(self.input_url, allow_redirects=True, timeout=5)

            # 만약 리디렉션이 정상적으로 되지 않으면 GET 요청으로 재시도
            if response.status_code >= 400 or response.url == self.input_url:
                response = requests.get(self.input_url, allow_redirects=True, timeout=5)

            # 최종 목적지 URL 저장
            self.original_url = response.url
        except requests.RequestException:
            # 요청 중 에러가 발생하면 None 처리
            self.original_url = None

    def scan(self):
        """
        전체 단축 URL 탐지 및 리디렉션 처리 흐름을 실행하는 함수
        """
        print("Module Start: [Shortened URL Detection]")

        if self.is_shortened_url():
            print(f"[Detected] Shortened URL : {self.input_url}")
            self.expand_url()

            if self.original_url:
                print(f"→ Redirected to: {self.original_url}")
            else:
                print("⚠ Redirection failed. Original URL could not be resolved.")
            
            print("\nModule End.")
            return True, self.original_url
        else:
            print(f"[Normal URL] {self.input_url}")
            print("\nModule End.")
            return False, self.input_url

# Module Main
if __name__ == "__main__":
    # Input : URL
    if len(sys.argv) != 2:
        print("How to Use : python3 url_shorting.py < URL >")
        sys.exit(1)
    
    input_url = sys.argv[1]
    detector = ShortenedURLDetector(input_url)
    is_shortened, expanded_url = detector.scan()
