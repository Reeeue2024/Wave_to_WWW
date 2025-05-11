# [ Kernel ] Module - JS : js_script_static.py

from core_engine.plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
import re

class JsScriptStatic(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.pattern_list = [
            {
                "pattern_type" : "inline_event_script",
                "pattern" : r"<script[^>]*>.*(onerror|onload|onclick)=.*</script>",
                "pattern_reason" : "Inline Event Script Exist."
            },
            {
                "pattern_type" : "data_uri_script",
                "pattern" : r"data:text/javascript",
                "pattern_reason" : "Data URI Script Exist."
            },
            {
                "pattern_type" : "document_write_script",
                "pattern" : r"document\.write(ln)?\s*\(",
                "pattern_reason" : "Document Write Script Exist."
            },
            {
                "pattern_type" : "base64_script",
                "pattern" : r"atob\s*\(|btoa\s*\(|[A-Za-z0-9+/]{50,}={0,2}",
                "pattern_reason" : "Base64 Script Exist."
            },
            {
                "pattern_type" : "image_tag_script",
                "pattern" : r"<img[^>]+src=['\"]javascript:",
                "pattern_reason" : "Image Tag Script Exist."
            },
            {
                "pattern_type" : "inline_image_tag_script",
                "pattern" : r"<script[^>]+src=.*?>.*?</script>",
                "pattern_reason" : "Inline Image Tag Script Exist."
            },
            {
                "pattern_type" : "iframe_script",
                "pattern" : r"<iframe[^>]+src=['\"]javascript:",
                "pattern_reason" : "Iframe Script Exist."
            },
            {
                "pattern_type" : "document_cookie_script",
                "pattern" : r"document\.cookie",
                "pattern_reason" : "Document Cookie Script Exist."
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

        script_tag = "\n".join(str(tag) for tag in bs.find_all("script"))

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
        self.module_result_data["reason"] = "JS Inject Pattern Not Exist."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_script_static.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsScriptStatic(input_url)

    module_instance.scan()
