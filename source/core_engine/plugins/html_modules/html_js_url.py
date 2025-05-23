# [ Kernel ] Module - HTML : html_js_url.py

from core_engine.plugins._base_module import BaseModule

import sys
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
    async def scan(self) :
        html_file_bs_object = self.engine_resource.get("html_file_bs_object")

        # Run Fail Case #1
        if not html_file_bs_object :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get HTML File from Engine."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        reason_list = []
        reason_data_list = []

        # To Do
        event_attribute_list = ["onclick", "onmouseover", "onload", "onfocus"]

        # [ 1. ] Event Attribute
        for event_attribute in event_attribute_list :

            for tag in html_file_bs_object.find_all(attrs = {event_attribute : True}) :

                tag_event_attribute = tag.get(event_attribute, "")

                if not tag_event_attribute :

                    continue

                for url_element in self.get_url_list(tag_event_attribute) :

                    if self.is_external_url(self.input_url, url_element) :

                        reason_list.append("External URL in Event Attribute.")
                        reason_data_list.append(url_element)

        # [ 2. ] Script Tag
        for script_tag in html_file_bs_object.find_all("script") :

            if script_tag.string :

                for url_element in self.get_url_list(script_tag.string) :

                    if self.is_external_url(self.input_url, url_element) :

                        reason_list.append("External URL in Script Tag.")
                        reason_data_list.append(url_element)

        # ( Run : True ) + ( Scan : True )
        if reason_list or reason_data_list :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = True
            self.module_result_data["reason"] = reason_list
            self.module_result_data["reason_data"] = reason_data_list

        # ( Run : True ) + ( Scan : False )
        else :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = False
            self.module_result_data["reason"] = "Not Exist External URL in Event Attribute and Script Tag."
            self.module_result_data["reason_data"] = None

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
