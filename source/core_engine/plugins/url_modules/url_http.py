# [ URL / Domain Modules ] HTTP 사용 여부를 바탕으로 탐지

import os
import sys

class HTTPUsageScorer:
    """
    IN : URL (string)
    OUT : 
        - score (float) : HTTP 사용 여부 기반 위험 점수 (0.0 ~ 1.0)
    """
    def __init__(self, input_url):
        # 입력된 URL 저장
        self.input_url = input_url

    def scan(self):
        """
        Step 1: HTTP/HTTPS 여부에 따라 위험 점수 부여
        - http://  → 점수 1.0 (위험)
        - https:// → 점수 0.0 (안전)
        - 기타      → 점수 None (형식 불명)
        """
        print("Module Start: [HTTP Usage Scoring]")

        if self.input_url.startswith("http://"):
            print(f"[Detected] HTTP URL: {self.input_url}")
            print(f"→ Score: 1.00 (0.0: Safe, 1.0: High Risk)")
            print("\nModule End.")
            return 1.0

        elif self.input_url.startswith("https://"):
            print(f"[Detected] HTTPS URL: {self.input_url}")
            print(f"→ Score: 0.00 (0.0: Safe, 1.0: High Risk)")
            print("\nModule End.")
            return 0.0

        else:
            print(f"[Warning] Unknown URL format: {self.input_url}")
            print("→ Score: None (unable to evaluate)")
            print("\nModule End.")
            return None

# Module Main
if __name__ == "__main__":
    # 입력 인자 수 확인
    if len(sys.argv) != 2:
        print("How to Use : python3 http_scorer.py < URL >")
        sys.exit(1)
    
    # URL 입력 및 점수 평가 실행
    input_url = sys.argv[1]
    scorer = HTTPUsageScorer(input_url)
    score = scorer.scan()
