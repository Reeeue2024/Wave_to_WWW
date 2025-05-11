# [ Kernel ] Module - HTML : html_js_url.py

from core_engine.plugins._base_module import BaseModule

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
    def is_external_url(self, one_url, two_url) :
        one_domain_suffix = self.get_domain_suffix(one_url)
        two_domain_suffix = self.get_domain_suffix(two_url)

        return one_domain_suffix != two_domain_suffix

    """
    IN : 
    OUT : 
    """
    def get_url_list(self, tag_event_attribute) :
        pattern = r"""['"](https?:?//[^'"]+)['"]"""

        return re.findall(pattern, tag_event_attribute)

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        html_file_bs_object = self.engine_resource.get("html_file_bs_object")

        event_attribute_list = ["onclick", "onmouseover", "onload", "onfocus"]

        # [ 1. ] Event Attribute
        for event_attribute in event_attribute_list :

            for tag in html_file_bs_object.find_all(attrs = {event_attribute : True}) :

                tag_event_attribute = tag.get(event_attribute, "")

                if not tag_event_attribute :

                    continue

                for url_element in self.get_url_list(tag_event_attribute) :

                    if self.is_external_url(self.input_url, url_element) :

                        self.module_result_flag = True
                        self.module_result_data["reason"] = "External URL in Event Attribute."
                        self.module_result_data["reason_data"] = url_element

                        self.create_module_result()

                        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                        return self.module_result_dictionary

        # [ 2. ] Script Tag
        for script_tag in html_file_bs_object.find_all("script") :

            if script_tag.string :

                for url_element in self.get_url_list(script_tag.string) :

                    if self.is_external_url(self.input_url, url_element) :

                        self.module_result_flag = True
                        self.module_result_data["reason"] = "External URL in Script Tag."
                        self.module_result_data["reason_data"] = url_element

                        self.create_module_result()

                        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                        return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Not Exist External URL in Event Attribute and Script Tag."
        self.module_result_data["reason_data"] = ""

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
