# [ JS Modules ] JS Redirect Dynamic Python

import os
import sys
import subprocess
import json

class JsRedirectDynamic:
    """
    IN  : URL (str)
    OUT : score (float) : 0.0 ~ 1.0
    """
    def __init__(self, input_url):
        self.input_url = input_url

    """
    IN  : URL
    OUT : Scan Result (True : Phishing O / False : Phishing X)
    """
    def scan(self):
        # print("Module Start: [JS Redirect Dynamic].")

        try:
            result = subprocess.run(
                ['node', 'js_redirect_dynamic.js', self.input_url],
                capture_output=True,
                text=True,
                timeout=15
            )

            lines = result.stdout.strip().split('\n')

            # 최종 URL 파싱
            final_url = None
            for line in lines:
                if "Final URL:" in line:
                    final_url = line.split("Final URL:")[1].strip()
                    break

            # JSON 추출
            json_line = next(line for line in lines if line.strip().startswith('{'))
            result_data = json.loads(json_line)

            logs = result_data.get("logs", [])
            score = result_data.get("score", 0)

            # 리디렉션 응답 코드 출력 (Python에서 직접 출력)
            for line in lines:
                if "Redirect response code detected:" in line:
                    print(f"[Info] Redirect Response Code: {line.split(':')[1].strip()}")  # [Info] 포맷

            # JS 로그에 의한 리디렉션 대상 추출
            redirect_targets = [
                line.split("Redirect detected:")[1].strip()
                for line in lines if "Redirect detected:" in line
            ]

            # JS 로그에는 없지만 최종 URL이 변경된 경우 → 강제 포함
            if not redirect_targets and any("Redirect detected" in log for log in logs):
                if final_url and final_url != self.input_url:
                    redirect_targets.append(final_url)

            # 리디렉션 정보 출력
            # print(f"[Detected] JS Redirect: {redirect_targets} (fast +{score})")
            # print(f"→ Score: {score:.1f} (0.0: Safe, 1.0: High Risk)")

            return score > 0.0  # 점수가 0 이상이면 위험 URL로 판단

        except Exception as e:
            # print("Error:", e)
            # print("→ Score: 0.0 (Fail)")
            return False

        # finally:
            # print("\nModule End.")


# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("How to Use : python3 js_redirect_dynamic.py < URL >")
        sys.exit(1)

    input_url = sys.argv[1]
    js_redirect_dynamic = JsRedirectDynamic(input_url)
    js_redirect_dynamic.scan()
