# [ JS Modules ] js_obfuscation_static.py

import requests
from bs4 import BeautifulSoup
import re

class JsObfuscationStatic:
    """
    IN  : URL
    OUT : 탐지 결과
    """
    def __init__(self, url):
        """
        초기화 및 탐지규칙 설정
        """
        self.url = url
        self.logs = []
        self.score = 0
        self.status = "안전"
        self.rules = [
    {
        "name": "base64_encoding",
        "pattern": r"atob\(|btoa\(",
        "score": 10,
        "message": "Base64 인코딩 감지"
    },
    {
        "name": "hex_encoding",
        "pattern": r"\\x[0-9a-fA-F]{2}",
        "score": 10,
        "message": "16진수 인코딩 감지"
    },
    {
        "name": "split_join_obfuscation",
        "pattern": r"(\"[a-zA-Z]\" *\+ *\"[a-zA-Z]\")",
        "score": 10,
        "message": "문자열 분할 후 합성 감지"
    },
    {
        "name": "reverse_join_obfuscation",
        "pattern": r"split\(.*\)\s*\.\s*reverse\(\)\s*\.\s*join\(\)",
        "score": 10,
        "message": "reverse + join 조합 감지"
    },
    {
        "name": "random_var_names",
        "pattern": r"var\s+_0x[a-f0-9]{4,}",
        "score": 10,
        "message": "무작위 변수명 패턴 감지"
    },
    {
        "name": "charcode_execution",
        "pattern": r"String\.fromCharCode\(",
        "score": 10,
        "message": "문자코드 기반 실행 가능성 감지"
    },
    {
        "name": "function_constructor",
        "pattern": r"new\s+Function\s*\(",
        "score": 10,
        "message": "Function 생성자 사용 감지"
    },
    {
        "name": "iife_detected",
        "pattern": r"\(function\s*\(.*\)\s*{.*}\)\s*\(\)",
        "score": 10,
        "message": "즉시 실행 함수 감지"
    },
    {
        "name": "self_invoking_wrapper",
        "pattern": r"var\s+\w+\s*=\s*function\s*\(.*\)\s*{.*};\s*\w+\(\)",
        "score": 10,
        "message": "자체 호출 래퍼 함수 감지"
    },
    {
        "name": "replace_function_obfuscation",
        "pattern": r"\.replace\(\s*\/.*\/\s*,\s*function\s*\(",
        "score": 10,
        "message": "정규표현식 + replace 함수 난독화 감지"
    }
]


    def run(self):
        """
        IN  : self.url
        OUT : {
            module: 모듈 이름,
            score : 총 탐지 점수,
            status: 안전 / 주의 / 위험,
            logs  : 탐지 로그 리스트
            }
        """
        try:
            response = requests.get(self.url, timeout=5)
            html = response.text
        except Exception as e:
            self.logs.append(f"[접속 실패] {self.url} → {str(e)} (+20점)")
            self.score += 20
            self.status = "주의"
            return self.result()

        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")
        js_code = "\n".join(script.text for script in scripts if script.text)

        for rule in self.rules:
            if re.search(rule["pattern"], js_code):
                self.logs.append(f"{rule['message']} (+{rule['score']}점)")
                self.score += rule["score"]

        if self.score >= 50:
            self.status = "위험"
        elif self.score >= 20:
            self.status = "주의"
        else:
            self.status = "안전"

        return self.result()

    def result(self):
        return {
            "module": "js_obfuscation_static",
            "score": self.score,
            "status": self.status,
            "logs": self.logs
        }

    def scan(self):
        result = self.run()
        for log in result["logs"]:
            print("[ 탐지 로그 ]", log)
        print(f"[ 탐지 결과 ] 총점: {result['score']}점")
        print(f"[ 탐지 결과 ] 위험도: {result['status']}")
        return result["status"] != "안전"
