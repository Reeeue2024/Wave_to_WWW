# [ Kernel ] Module - JS : js_static_script.py

from core_engine.plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
import re

class JsStaticScript(BaseModule) :
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
                "pattern_type" : "script_dom_write",
                "pattern" : r"document\.write(ln)?\s*\(\s*['\"].*<script.*?>.*?<\/script>.*['\"]",
                "pattern_reason" : "Exist \"document.write()\" Inject Script in JS."
            },
            {
                "pattern_type" : "script_innerhtml_inject",
                "pattern" : r"(innerHTML|insertAdjacentHTML)\s*=\s*['\"].*<script.*?>.*?<\/script>.*['\"]",
                "pattern_reason" : "Exist \"innerHTML / insertAdjacentHTML\" Inject Script in JS."
            },
            {
                "pattern_type" : "script_createElement_inject",
                "pattern" : r"document\.createElement\s*\(\s*['\"]script['\"]\s*\)",
                "pattern_reason" : "Exist \"document.createElement()\" Inject Script in JS."
            },
            {
                "pattern_type" : "script_dom_append",
                "pattern" : r"(appendChild|append)\s*\(\s*.*script.*\)",
                "pattern_reason" : "Exist Element Append to DOM Script in JS."
            },
            {
                "pattern_type" : "script_src_assign",
                "pattern" : r"\.src\s*=\s*['\"]http[s]?://[^'\"]+['\"]",
                "pattern_reason" : "Exist Source Assign Script in JS."
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
        self.module_result_data["reason"] = "Not Exist Script Pattern in JS."
        self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_static_script.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsStaticScript(input_url)

    module_instance.scan()
