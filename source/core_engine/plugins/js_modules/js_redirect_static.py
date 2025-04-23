# [ JS Modules ] Redirect Static

import sys
import requests
import re

class JsRedirectStatic:
    """
    IN  : URL (str)
    OUT : score (float) : 0.0 ~ 1.0
    """

    def __init__(self, input_url):
        self.input_url = input_url

    def scan(self):
        # print("Module Start: [JS Redirect Static]")

        try:
            response = requests.get(self.input_url)
            response.raise_for_status()
            js_code = response.text

            # 리다이렉션 관련 패턴 정의
            patterns = [
                r"window\.location\s*=\s*['\"](http[s]?://[^'\"]+)['\"]",
                r"window\.location\.href\s*=\s*['\"](http[s]?://[^'\"]+)['\"]",
                r"window\.location\.assign\s*\(['\"](http[s]?://[^'\"]+)['\"]\)",
                r"location\.replace\s*\(['\"](http[s]?://[^'\"]+)['\"]\)",
                r"location\.assign\s*\(['\"](http[s]?://[^'\"]+)['\"]\)",
                r"document\.location\s*=\s*['\"](http[s]?://[^'\"]+)['\"]",
                r"document\.location\.href\s*=\s*['\"](http[s]?://[^'\"]+)['\"]",
                r"top\.location\s*=\s*['\"](http[s]?://[^'\"]+)['\"]",
                r"top\.location\.href\s*=\s*['\"](http[s]?://[^'\"]+)['\"]",
                r"self\.location\s*=\s*['\"](http[s]?://[^'\"]+)['\"]",
            ]

            redirect_urls = []

            for pattern in patterns:
                matches = re.findall(pattern, js_code)
                redirect_urls.extend(matches)

            if redirect_urls:
                # print(f"[Detected] JS Redirect: {redirect_urls}")
                # print(f"→ Score: 1.0 (0.0: Safe, 1.0: High Risk)")
                # print("\nModule End.")
                return True
            else:
                # print(f"[Normal] No JS Redirect: {self.input_url}")
                # print("→ Score: 0.0 (0.0: Safe, 1.0: High Risk)")
                # print("\nModule End.")
                return False

        except requests.RequestException as e:
            # print(f"[ERROR] Failed to fetch JS file: {e}")
            # print("→ Score: 0.0 (0.0: Safe, 1.0: High Risk)")
            # print("\nModule End.")
            return False


# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("How to Use : python3 js_redirect_static.py <JS URL>")
        sys.exit(1)

    input_url = sys.argv[1]
    js_redirect_static = JsRedirectStatic(input_url)
    js_redirect_static.scan()
