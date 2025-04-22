# [ JS Modules ] External Server Dynamic Python

import os
import sys
import subprocess
import json
import shlex

class JsExfilDynamic:
    """
    IN  : URL (str)
    OUT : score (float) : 0.0 ~ 1.0
    """

    def __init__(self, input_url):
        self.input_url = input_url
        self.js_script_path = os.path.join(os.path.dirname(__file__), 'js_exfil_dynamic.js')

    """
    IN  : URL
    OUT : Scan Result (True : Phishing O / False : Phishing X)
    """
    def scan(self):
        # print("Module Start: [JS Exfil Dynamic]")

        if not os.path.exists(self.js_script_path):
            return self._handle_error("JavaScript analysis file not found.")

        try:
            # Node.js 명령어 실행
            result = subprocess.run(
                ['node', self.js_script_path, self.input_url],
                capture_output=True,
                text=True,
                timeout=45
            )

            if result.returncode != 0:
                return self._handle_error(f"Node.js script exited with code {result.returncode}", result.stderr)

            # JSON 출력 파싱
            result_data = self._parse_json(result.stdout)
            if not result_data:
                return self._handle_error("No valid JSON output from Node.js.")

            score = float(result_data.get("score", 0.0))
            detected_requests = result_data.get("detected_requests", [])

            # 결과 출력
            # if detected_requests:
            #     print(f"[Detected] JS Exfil: {detected_requests[:5]} (+{score:.1f})")
            # else:
            #     print(f"[Detected] No JS Exfil. (+{score:.1f})")

            return score > 0.0  # 외부 요청이 있으면 True

        except subprocess.TimeoutExpired:
            return self._handle_error("Node.js script timed out after 45 seconds.")
        except Exception as e:
            return self._handle_error(f"Unexpected error: {e}")

        # finally:
        #     print("\nModule End.")

    def _parse_json(self, stdout):
        """
        IN  : stdout (str) : Node.js의 출력
        OUT : Parsed JSON (dict) or None
        """
        try:
            lines = stdout.strip().split('\n')
            for line in lines:
                if line.startswith('{') and line.endswith('}'):
                    return json.loads(line)  # 유효한 JSON 반환
        except json.JSONDecodeError:
            return None

    def _handle_error(self, message, stderr=None):
        """
        IN  : message (str) : 오류 메시지
        OUT : False
        """
        # print(f"[Error] {message}")
        if stderr:
        #     print(f"[Error Details] {stderr.strip()}")
        # print("→ Score: 0.0 (Fail)")
            return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("Usage: python3 js_exfil_dynamic.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    js_exfil_dynamic = JsExfilDynamic(input_url)
    result = js_exfil_dynamic.scan()

    sys.exit(0 if result else 1)
