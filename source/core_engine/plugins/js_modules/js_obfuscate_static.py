# [ Kernel ] Module - JS : js_obfuscate_static.py

from core_engine.plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
import re

class JsObfuscateStatic(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.pattern_list = [
            {
                "pattern_type" : "base64_obfuscate",
                "pattern" : r"atob\(|btoa\(",
                "pattern_reason" : "Base64 Obfuscate Exist."
            },
            {
                "pattern_type" : "hex_obfuscate",
                "pattern" : r"\\x[0-9a-fA-F]{2}",
                "pattern_reason" : "Hex Obfuscate Exist."
            },
            {
                "pattern_type" : "split_join_obfuscate",
                "pattern" : r"(\"[a-zA-Z]\" *\+ *\"[a-zA-Z]\")",
                "pattern_reason" : "String Split + Join Obfuscate Exist."
            },
            {
                "pattern_type" : "reverse_join_obfuscate",
                "pattern" : r"split\(.*\)\s*\.\s*reverse\(\)\s*\.\s*join\(\)",
                "pattern_reason" : "Reverse + Join Obfuscate Eist."
            },
            {
                "pattern_type" : "random_variable_name_obfuscate",
                "pattern" : r"var\s+_0x[a-f0-9]{4,}",
                "pattern_reason" : "Random Variable Name Obfuscate Exist."
            },
            {
                "pattern_type" : "character_code_obfuscate",
                "pattern" : r"String\.fromCharCode\(",
                "pattern_reason" : "Character Code Obfuscate Exist."
            },
            {
                "pattern_type" : "new_function_obfuscate",
                "pattern" : r"new\s+Function\s*\(",
                "pattern_reason" : "New Function Obfuscate Exist."
            },
            {
                "pattern_type" : "iife_obfuscate",
                "pattern" : r"\(function\s*\(.*\)\s*{.*}\)\s*\(\)",
                "pattern_reason" : "IIFE Obfuscate Exist."
            },
            {
                "pattern_type" : "self_invoke_function_obfuscate",
                "pattern" : r"var\s+\w+\s*=\s*function\s*\(.*\)\s*{.*};\s*\w+\(\)",
                "pattern_reason" : "Self Invoke Function Obfuscate Exist."
            },
            {
                "pattern_type" : "replace_function_obfuscate",
                "pattern" : r"\.replace\(\s*\/.*\/\s*,\s*function\s*\(",
                "pattern_reason" : "Replace Function Obfuscate Exist."
            }
        ]

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        try :
            response = requests.get(self.input_url, timeout = 5)

            response.raise_for_status()

            html = response.text

        except requests.RequestException as e :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Fail to Get HTML."

            self.create_module_result()

            return self.module_result_dictionary

        bs = BeautifulSoup(html, "html.parser")

        script_text = "\n".join(script.text for script in bs.find_all("script") if script.text)

        for pattern_element in self.pattern_list :

            pattern_result = re.search(pattern_element["pattern"], script_text, re.IGNORECASE | re.DOTALL)

            if pattern_result :

                reason_data = pattern_result.group(0).strip()

                self.module_result_flag = True
                self.module_result_data["pattern_type"] = pattern_element["pattern_type"]
                self.module_result_data["pattern"] = pattern_element["pattern"]
                self.module_result_data["reason"] = reason_data

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Obfuscate Pattern Not Exist."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_obfuscate_static.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsObfuscateStatic(input_url)

    module_instance.scan()
