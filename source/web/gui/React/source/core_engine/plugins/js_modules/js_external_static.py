# [ Core ] Module - JS : js_external_static.py

from plugins._base_module import BaseModule

import sys
import requests
import re

class JsExternalStatic(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.pattern_list = [
            {
                "pattern_type" : "external_fetch",
                "pattern" : rf"fetch\s*\(\s*['\"]http[s]?://(?!{re.escape(self.input_url)}).*?['\"]",
                "pattern_reason" : "External Fetch Exist."
            },
            {
                "pattern_type" : "external_beacon",
                "pattern" : rf"navigator\.sendBeacon\s*\(\s*['\"]http[s]?://(?!{re.escape(self.input_url)}).*?['\"]",
                "pattern_reason" : "External Beacon Exist."
            },
            {
                "pattern_type" : "external_xmlhttprequest",
                "pattern" : rf"new\s+XMLHttpRequest\s*\(\s*\).*?open\s*\(\s*['\"]POST['\"]?,\s*['\"]http[s]?://(?!{re.escape(self.input_url)}).*?['\"]",
                "pattern_reason" : "External XMLHttpRequest Exist."
            },
            {
                "pattern_type" : "external_image_request",
                "pattern" : rf"(new\s+Image\(\)|img\.src)\s*=\s*['\"]http[s]?://(?!{re.escape(self.input_url)}).*?['\"]",
                "pattern_reason" : "External Image Request Exist."
            },
            {
                "pattern_type" : "prevent_default",
                "pattern" : r"\.preventDefault\s*\(\s*\)",
                "pattern_reason" : "Prevent Default Exist."
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
            self.module_result_data["reason"] = f"Fail to Get HTML."

            self.create_module_result()

            return self.module_result_dictionary

        for pattern_element in self.pattern_list :

            pattern_result = re.search(pattern_element["pattern"], html, re.IGNORECASE | re.DOTALL)

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
        self.module_result_data["reason"] = "External Pattern Not Exist."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_external_static.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsExternalStatic(input_url)

    module_instance.scan()