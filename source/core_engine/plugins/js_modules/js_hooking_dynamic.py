# [ JS Modules ] Hooking Dynamic Python

import subprocess
import json
import sys

class JsHookingDynamic:
    """
    IN  : URL (str)
    OUT : score (float) : 0.0 ~ 1.0
    """
    def __init__(self, input_url):
        self.input_url = input_url

    def scan(self):
        """
        IN : URL
        OUT : Scan Result (True : Phishing O / False : Phishing X)
        """
        # print("Module Start: [JS Hooking Dynamic]")

        try:
            result = subprocess.run(
                ['node', 'js_hooking_dynamic.js', self.input_url],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                # print(f"오류 발생: {result.stderr}")
                return False

            event_data = json.loads(result.stdout)
            logs = event_data.get('logs', [])
            score = float(event_data.get('score', 0.0))

            if logs:
                # print(f"[Detected] JS Hooking: {logs}")
                return True
            else:
                # print("[Normal] No JS Hooking")
                return False

        except Exception:
            # print("Puppeteer error or invalid JSON.")
            return False


# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("How to Use : python3 js_hooking_dynamic.py <URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    js_hooking_dynamic = JsHookingDynamic(input_url)
    result = js_hooking_dynamic.scan()

    # 명시적 종료 코드 전달
    sys.exit(0 if result else 1)
