# [ Core ] Module - JS : js_redirect_static.py

from plugins._base_module import BaseModule

import sys
import requests
import re

class JsRedirectStatic(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.pattern_list = [
            {
                "pattern_type" : "redirect_window_location",
                "pattern" : r"window\.location\s*=\s*['\"]http[s]?://[^'\"]+['\"]",
                "pattern_reason" : "window.location Redirect Exist."
            },
            {
                "pattern_type" : "redirect_window_location_href",
                "pattern" : r"window\.location\.href\s*=\s*['\"]http[s]?://[^'\"]+['\"]",
                "pattern_reason" : "window.location.href Redirect Exist."
            },
            {
                "pattern_type" : "redirect_window_location_assign",
                "pattern" : r"window\.location\.assign\s*\(['\"]http[s]?://[^'\"]+['\"]\)",
                "pattern_reason" : "window.location.assign Redirect Exist."
            },
            {
                "pattern_type" : "redirect_location_replace",
                "pattern" : r"location\.replace\s*\(['\"]http[s]?://[^'\"]+['\"]\)",
                "pattern_reason" : "location.replace Redirect Exist."
            },
            {
                "pattern_type" : "redirect_document_location",
                "pattern" : r"document\.location\s*=\s*['\"]http[s]?://[^'\"]+['\"]",
                "pattern_reason" : "document.location Redirect Exist."
            },
            {
                "pattern_type" : "redirect_document_location_href",
                "pattern" : r"document\.location\.href\s*=\s*['\"]http[s]?://[^'\"]+['\"]",
                "pattern_reason" : "document.location.href Redirect Exist."
            },
            {
                "pattern_type" : "redirect_top_location",
                "pattern" : r"top\.location\s*=\s*['\"]http[s]?://[^'\"]+['\"]",
                "pattern_reason" : "top.location Redirect Exist."
            },
            {
                "pattern_type" : "redirect_self_location",
                "pattern" : r"self\.location\s*=\s*['\"]http[s]?://[^'\"]+['\"]",
                "pattern_reason" : "self.location Redirect Exist."
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
        self.module_result_data["reason"] = "JS Redirect Pattern Not Exist."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_redirect_static.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsRedirectStatic(input_url)

    module_instance.scan()
