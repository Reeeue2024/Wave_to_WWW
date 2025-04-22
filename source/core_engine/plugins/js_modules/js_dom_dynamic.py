# [Python Modules] js_dom_dynamic.py

import subprocess
import json
import os

class JsDomDynamic:
    """
    IN  : URL
    OUT : 탐지 결과
    """
    def __init__(self, url):
        self.url = url
        self.logs = []
        self.score = 0
        self.status = "안전"

    def run(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        js_path = os.path.abspath(os.path.join(script_dir, "js_dom_dynamic.js"))

        result_json = ""

        try:
            result_json = subprocess.check_output(
                ["node", js_path, self.url],
                universal_newlines=True,
                timeout=10
            )
        except subprocess.TimeoutExpired:
            self.logs.append("[오류] JS 실행 타임아웃 (+20점)")
            self.score += 20
        except Exception as e:
            self.logs.append(f"[오류] JS 실행 실패: {str(e)} (+20점)")
            self.score += 20

        if result_json:
            try:
                result = json.loads(result_json)
                self.logs.extend(result.get("logs", []))
                self.score += int(result.get("score", 0))
            except json.JSONDecodeError:
                self.logs.append("[오류] JS 결과 파싱 실패 (+20점)")
                self.score += 20

        if self.score >= 50:
            self.status = "위험"
        elif self.score >= 20:
            self.status = "주의"
        else:
            self.status = "안전"

        return {
            "module": "DOM Change Detector (Dynamic)",
            "score": self.score,
            "status": self.status,
            "logs": self.logs
        }

    def scan(self):
        result = self.run()
        # for log in result["logs"]:
        #     print("[ 탐지 로그 ]", log)
        # print(f"[ 탐지 결과 ] 총점: {result['score']}점")
        # print(f"[ 탐지 결과 ] 위험도: {result['status']}")
        # print("--------------------")
        return result["status"] != "안전"
