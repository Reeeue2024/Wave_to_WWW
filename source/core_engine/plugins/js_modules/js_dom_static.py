# [ Core ] Module - JS : js_dom_static.py

from plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

class JsDomStatic(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.pattern_list = [
            {
                "pattern_type" : "hide_iframe",
                "pattern" : r'<iframe[^>]*(display:\s*none|visibility:\s*hidden|width=["\']?0["\']?|height=["\']?0["\']?)',
                "pattern_reason" : "Hide Iframe Exist."
            },
            {
                "pattern_type" : "external_script",
                "pattern" : rf'<script[^>]+src=["\'](http|https)://(?!.*{re.escape(urlparse(self.input_url).netloc)})',
                "pattern_reason" : "External Script Exist."
            },
            {
                "pattern_type" : "external_form",
                "pattern" : rf'<form[^>]+action=["\'](http|https)://(?!.*{re.escape(urlparse(self.input_url).netloc)})',
                "pattern_reason" : "External Form Exist."
            },
            {
                "pattern_type" : "http_form",
                "pattern" : r'<form[^>]+action=["\']http://[^>]*>.*?<input[^>]*type=["\']password["\']',
                "pattern_reason" : "HTTP Form Exist."
            },
            {
                "pattern_type" : "hide_link",
                "pattern" : r'<a[^>]*(display:\s*none|visibility:\s*hidden|width=["\']?0["\']?|height=["\']?0["\']?)',
                "pattern_reason" : "Hide Link Exist."
            },
            {
                "pattern_type" : "redirect_iframe",
                "pattern" : rf'<iframe[^>]+src=["\'](http|https)://(?!.*{re.escape(urlparse(self.input_url).netloc)})',
                "pattern_reason" : "Redirect Iframe Exist."
            },
            {
                "pattern_type" : "meta_refresh",
                "pattern" : r'<meta[^>]+http-equiv=["\']refresh["\'][^>]+content=["\']\d+;\s*url=',
                "pattern_reason" : "Meta Refresh Exist."
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

        except Exception as e :
            self.module_result_flag = False
            self.module_result_data["reason"] = f"Fail to Get HTML."

            self.create_module_result()

            return self.module_result_dictionary

        bs = BeautifulSoup(html, "html.parser")

        dom = str(bs)

        for pattern_element in self.pattern_list :

            pattern_result = re.search(pattern_element["pattern"], dom, re.IGNORECASE | re.DOTALL)

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
        self.module_result_data["reason"] = "DOM Pattern Not Exist."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_dom_static.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsDomStatic(input_url)

    module_instance.scan()
