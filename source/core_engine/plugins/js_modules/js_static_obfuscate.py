# [ Kernel ] Module - JS : js_static_obfuscate.py

from core_engine.plugins._base_module import BaseModule

import sys
import re

class JsStaticObfuscate(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

    """
    IN : 
    OUT : 
    """
    async def scan(self) :
        html_file_script_tag_list = self.engine_resource.get("html_file_script_tag_list", [])
        js_file_dictionary_list = self.engine_resource.get("js_file_dictionary_list", {})

        if not html_file_script_tag_list or not js_file_dictionary_list :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get HTML File / JS File from Engine."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        js_code_list = html_file_script_tag_list[:]
        js_code_list.extend(js_file_dictionary_list.values())

        all_js_code = "\n".join(js_code_list)

        pattern_list = [
            {
                "pattern_type" : "obfuscate_base64",
                "pattern" : r"(?:atob|btoa)\s*\(\s*[^)]+\s*\)",
                "pattern_reason" : "Exist Base64 Obfuscate in JS."
            },
            {
                "pattern_type" : "obfuscate_hex",
                "pattern" : r"\\x[0-9a-fA-F]{2}",
                "pattern_reason" : "Exist Hex Obfuscate in JS."
            },
            {
                "pattern_type" : "obfuscate_split_join",
                "pattern" : r"(['\"][a-zA-Z]{1,3}['\"]\s*\+\s*['\"][a-zA-Z]{1,3}['\"])(\s*\+\s*['\"][a-zA-Z]{1,3}['\"])*",
                "pattern_reason" : "Exist String Split + Join Obfuscate in JS."
            },
            {
                "pattern_type" : "obfuscate_reverse_join",
                "pattern" : r"[\"'][^\"']+[\"']\s*\.split\s*\(\s*[\"'].*?[\"']\s*\)\s*\.reverse\s*\(\)\s*\.join\s*\(\s*[\"']?.*?[\"']?\s*\)",
                "pattern_reason" : "Exist Reverse + Join Obfuscate in JS."
            },
            {
                "pattern_type" : "obfuscate_random_variable_name",
                "pattern" : r"\bvar\s+_0x[a-f0-9]{4,}\b",
                "pattern_reason" : "Exist Random Variable Name Obfuscate in JS."
            },
            {
                "pattern_type" : "obfuscate_character_code",
                "pattern" : r"String\.fromCharCode\s*\(\s*[0-9,\s]+\)",
                "pattern_reason" : "Exist Character Code Obfuscate in JS."
            },
            {
                "pattern_type" : "obfuscate_new_function",
                "pattern" : r"new\s+Function\s*\(\s*(['\"].*?['\"]\s*,\s*)*['\"].*?['\"]\s*\)",
                "pattern_reason" : "Exist New Function Obfuscate in JS."
            },
            {
                "pattern_type" : "obfuscate_replace_function",
                "pattern" : r"\.replace\s*\(\s*/.*?/\s*,\s*function\s*\([^)]*\)\s*{[^}]*}\s*\)",
                "pattern_reason" : "Exist Replace Function Obfuscate in JS."
            },
        ]

        for pattern_element in pattern_list :

            pattern_result = re.search(pattern_element["pattern"], all_js_code, re.IGNORECASE | re.DOTALL)

            if pattern_result :

                reason_data = pattern_result.group(0).strip()

                self.module_run = True
                self.module_error = None
                self.module_result_flag = True
                self.module_result_data["reason"] = pattern_element["pattern_reason"]
                self.module_result_data["reason_data"] = reason_data

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        self.module_run = True
        self.module_error = None
        self.module_result_flag = False
        self.module_result_data["reason"] = "Not Exist Obfuscate Pattern in JS."
        self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_static_obfuscate.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsStaticObfuscate(input_url)

    module_instance.scan()
