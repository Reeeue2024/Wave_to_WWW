# [ URL / Domain Modules ] URL Shorting

# 이 모듈은 "리디렉션을 따라가서 최종 URL을 얻는다"까지만 함
# 피싱 판별 등은 다른 모듈로 넘김

import os
import sys
import re
import requests

class UrlShorting:
    """
    IN  : input_url (str) - 검사 대상 URL
    OUT : is_shortened (bool) - 단축 URL 여부
          expanded_url (str) - 리디렉션된 원본 URL (단축일 경우)
    """
    def __init__(self, input_url=None):
        self.input_url = input_url
        self.original_url = None

        # 단축 URL 도메인 목록
        self.short_url_domains = [
            # 기존 기본 도메인
            "bit.ly", "goo.gl", "t.co", "ow.ly", "tinyurl.com",
            "is.gd", "buff.ly", "adf.ly", "bit.do", "mcaf.ee",
            "rebrand.ly", "su.pr", "shorte.st", "cli.gs", "v.gd",

            # 추가된 도메인
            "url.kr", "buly.kr", "alie.kr", "link24.kr", "lrl.kr",
            "tr.ee", "t.ly", "t.me", "rb.gy", "shrtco.de",
            "chilp.it", "cutt.ly", "vvd.bz", 'IRI.MY', 'LINC.kr', 'abit.ly', 'chzzk.me', 'flic.kr',
            'glol.in', 'gourl.kr', 'han.gl', 'juso.ga', 'muz.so',
            'na.to', 'site.naver.com', 't2m.kr', 'tny.kr', 'tuney.kr',
            'twr.kr', 'ual.kr', 'url.sg', 'vo.la', 'wo.to',
            'yao.ng', 'zed.kr', 'zxcv.be'
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
        IN  : self.input_url (str) - 단축 URL
        OUT : self.original_url (str or None) - 리디렉션된 최종 URL
        """
        try:
            response = requests.get(self.input_url, allow_redirects=True, timeout=5)
            self.original_url = response.url
        except requests.RequestException:
            self.original_url = None

    def scan(self, input_url=None):
        """
        IN : input_url
        OUT : Scan Result (True : 단축 URL / False : 일반 URL)
        """
        
        if input_url:
            self.input_url = input_url
        if not self.input_url:
            raise ValueError("No URL provided to scan.")

        # print("Module Start: [URL Shorting]")

        if self.is_shortened_url():
            # print(f"[Detected] Shortened URL : {self.input_url}")
            # self.expand_url()
            # if self.original_url:
            #    print(f"→ Redirected to: {self.original_url}")
            # else:
            #    print("Redirection failed. Original URL could not be resolved.")
            # print("\nModule End.")
            return True
        else:
            # print(f"[Normal URL] {self.input_url}")
            # print("\nModule End.")
            return False


# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("How to Use : python3 url_shorting.py < URL >")
        sys.exit(1)
    
    input_url = sys.argv[1]
    detector = UrlShorting()
    is_shortened = detector.scan(input_url)