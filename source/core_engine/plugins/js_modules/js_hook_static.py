# [ Core ] Module - JS : js_hook_static.py

from plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # InsecureRequestWarning

class JsHookStatic(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.pattern_list = [
            {
                "pattern_type" : "addEventListener",
                "pattern" : r"addEventListener",
                "pattern_reason" : "\"addEventListener\" Exist."
            },
            {
                "pattern_type" : "onclick",
                "pattern" : r"onclick",
                "pattern_reason" : "\"onclick\" Exist."
            },
            {
                "pattern_type" : "onkeydown",
                "pattern" : r"onkeydown",
                "pattern_reason" : "\"onkeydown\" Exist."
            },
            {
                "pattern_type" : "onkeyup",
                "pattern" : r"onkeyup",
                "pattern_reason" : "\"onkeyup\" Exist."
            },
            {
                "pattern_type" : "MutationObserver",
                "pattern" : r"MutationObserver",
                "pattern_reason" : "\"MutationObserver\" Exist."
            },
            {
                "pattern_type" : "fetch",
                "pattern" : r"fetch",
                "pattern_reason" : "\"fetch\" Exist."
            },
            {
                "pattern_type" : "XMLHttpRequest",
                "pattern" : r"XMLHttpRequest",
                "pattern_reason" : "\"XMLHttpRequest\" Exist."
            },
            {
                "pattern_type" : "eval",
                "pattern" : r"eval",
                "pattern_reason" : "\"eval\" Exist."
            },
            {
                "pattern_type" : "unescape",
                "pattern" : r"unescape",
                "pattern_reason" : "\"unescape\" Exist."
            },
            {
                "pattern_type" : "atob",
                "pattern" : r"atob",
                "pattern_reason" : "\"atob\" Exist."
            }
        ]

    """
    IN : 
    OUT : 
    """
    def scan_html(self, html) :
        bs = BeautifulSoup(html, "html.parser")

        script_list = bs.find_all("script")

        for script in script_list :

            if script.string :

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
        self.module_result_data["reason"] = "JS Hooking Pattern Not Exist in HTML."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

    """
    IN : 
    OUT : 
    """
    def scan_js(self, js) :
        for pattern_element in self.pattern_list :

            pattern_result = re.search(pattern_element["pattern"], js, re.IGNORECASE | re.DOTALL)

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
        self.module_result_data["reason"] = "JS Hooking Pattern Not Exist in JS."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary
    
    """
    IN : 
    OUT : 
    """
    def scan(self) :
        try :
            response = requests.get(self.input_url, verify = False, timeout = 5)

            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            if "html" in content_type :

                return self.scan_html(response.text)

            elif "javascript" in content_type or self.input_url.endswith(".js") :

                return self.scan_js(response.text)

        except requests.RequestException as e :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Fail to Get HTML / JS File."

            self.create_module_result()

            return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Fail to Get Content Type."

        self.create_module_result()

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_hook_static.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsHookStatic(input_url)

    module_instance.scan()
