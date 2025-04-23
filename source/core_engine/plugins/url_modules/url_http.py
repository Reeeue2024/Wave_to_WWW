# [ URL / Domain Modules ] HTTP/HTTPS

import os
import sys

class UrlHttp:
    """
    IN  : input_url (str) - 검사 대상 URL
    OUT : Scan Result
        - True  : HTTP URL (비암호화, 위험)
        - False : HTTPS URL (암호화, 안전)
        - None  : Unknown Format (평가 불가)
    """
    def __init__(self, input_url):
        # 입력된 URL 저장
        self.input_url = input_url

    def scan(self):
        """
        HTTP/HTTPS 여부에 따라 위험 점수
        - http://  → return 1.0 (True 취급)
        - https:// → return 0.0  (False 취급)
        - 기타      → return None (False 취급)
        """
        # print("Module Start: [URL HTTP/HTTPS]")

        if self.input_url.startswith("http://"):
            # print(f"[Detected] HTTP URL: {self.input_url}")
            # print(f"→ Score: 1.00 (0.0: Safe, 1.0: High Risk)")
            # print("\nModule End.")
            return True

        elif self.input_url.startswith("https://"):
            # print(f"[Detected] HTTPS URL: {self.input_url}")
            # print(f"→ Score: 0.00 (0.0: Safe, 1.0: High Risk)")
            # print("\nModule End.")
            return False

        else:
            # print(f"[Warning] Unknown URL format: {self.input_url}")
            # print("→ Score: None (unable to evaluate)")
            # print("\nModule End.")
            return False

# Module Main
if __name__ == "__main__":
    # 입력 인자 수 확인
    if len(sys.argv) != 2:
        print("How to Use : python3 url_http.py < URL >")
        sys.exit(1)
    
    # URL 입력 및 점수 평가 실행
    input_url = sys.argv[1]
    scorer = UrlHttp(input_url)
    score = scorer.scan()