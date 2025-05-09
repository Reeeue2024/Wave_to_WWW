# [ Core ] Module - HTML : html_js_url.py

# JS Event / Script → External Domain URL

from plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
import re

class HtmlJsUrl(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

    """
    IN : 
    OUT : 
    """
    def get_domain_suffix(self, url) :
        tldextract_result = tldextract.extract(url)

        return f"{tldextract_result.domain}.{tldextract_result.suffix}"

    """
    IN : 
    OUT : 
    """
    def is_external_domain(self, base_url, input_url) :
        base_domain = self.get_domain_suffix(base_url)

        input_domain = self.get_domain_suffix(input_url)

        return base_domain != input_domain

    """
    IN : 
    OUT : 
    """
    def get_url_list(self, js_code) :
        pattern = r"""['"]((http|https)://[a-zA-Z0-9\-._~:/?#@!$&'()*+,;=%]+)['"]"""

        return [pattern_result[0] for pattern_result in re.findall(pattern, js_code)]

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        headers = {
            "User-Agent" : "Mozilla/5.0"
        }

        try :
            response = requests.get(self.input_url, headers = headers, timeout = 5)

            response.raise_for_status()

            html = response.text

        except requests.RequestException as e :
            self.module_result_flag = False

            self.module_result_data["reason"] = "Fail to Get HTML."

            self.create_module_result()

            return self.module_result_dictionary

        bs = BeautifulSoup(html, "html.parser")

        base_url = self.input_url

        event_attribute_list = ["onclick", "onmouseover", "onload", "onfocus"]

        for event_attribute in event_attribute_list :

            # [ 1. ] Event Attribute
            for tag in bs.find_all(attrs = {event_attribute : True}) :

                js_code = tag.get(event_attribute, "")

                if not js_code :

                    continue

                for url_element in self.get_url_list(js_code) :

                    if self.is_external_domain(base_url, url_element) :

                        self.module_result_flag = True
                        self.module_result_data["reason"] = "External URL in Event Attribute."
                        self.module_result_data["url"] = url_element

                        self.create_module_result()

                        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                        return self.module_result_dictionary

        # [ 2. ] Script Tag
        for script_element in bs.find_all("script") :

            if script_element.string :

                for url_element in self.get_url_list(script_element.string) :

                    if self.is_external_domain(base_url, url_element) :

                        self.module_result_flag = True
                        self.module_result_data["reason"] = "External URL in Script Tag."
                        self.module_result_data["url"] = url_element

                        self.create_module_result()

                        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                        return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Not External URL."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_js_url.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlJsUrl(input_url)

    module_instance.scan()
