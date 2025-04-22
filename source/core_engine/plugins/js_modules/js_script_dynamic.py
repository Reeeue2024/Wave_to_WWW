# [ JS Modules ] obfuscation_detector_dynamic

import subprocess
import json
import os

class JsScriptDynamic:
    """
    IN  : URL
    OUT : 탐지 결과
    """
    def __init__(self, url):
        """
        초기화
        """
        self.url = url
        self.logs = []
        self.score = 0
        self.status = "안전"

    def run(self):
        """
        IN  : self.url
        OUT : {
            module: 모듈 이름,
            score : 누적 점수,
            status: 안전 / 주의 / 위험,
            logs  : 탐지 로그 리스트
            }
        - Node.js 기반 JS 파일 실행 (puppeteer 사용)
        - JS 실행 결과(JSON)를 파싱하여 점수 및 로그 수집
        - 예외 발생 시 로그 및 점수 반영
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        js_path = os.path.abspath(os.path.join(script_dir, "js_script_dynamic.js"))

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
                self.logs.append("[오류] JS 결과 파싱 실패 (+10점)")
                self.score += 10

        if self.score >= 50:
            self.status = "위험"
        elif self.score >= 20:
            self.status = "주의"
        else:
            self.status = "안전"

        return {
            "module": "Script Injection Detector (Dynamic)",
            "score": self.score,
            "status": self.status,
            "logs": self.logs
        }

    def scan(self):
        """
        - run() 실행 결과를 바탕으로 로그와 위험도 출력
        - 최종 위험도에 따라 Boolean 결과 반환
        """
        result = self.run()
        for log in result["logs"]:
            print("[ 탐지 로그 ]", log)
        print(f"[ 탐지 결과 ] 총점: {result['score']}점")
        print(f"[ 탐지 결과 ] 위험도: {result['status']}")
        print("--------------------")
        return result["status"] != "안전"
