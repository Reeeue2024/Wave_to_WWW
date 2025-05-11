# [ Kernel ] Module - HTML : html_meta_refresh.py

from core_engine.plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract
import re

class HtmlMetaRefresh(BaseModule) :
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
    def get_redirect_url(self, content) :
        pattern_result = re.search(r"url\s*=\s*[\"']?([^\"';\s]+)", content, re.IGNORECASE)

        if pattern_result :

            return pattern_result.group(1)

        return None

    """
    IN : 
    OUT : 
    """
    def get_redirect_delay(self, content) :
        try :
            delay_data = content.split(";")[0]

            return float(delay_data.strip())

        except :
            return 999.0

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        html_file_bs_object = self.engine_resource.get("html_file_bs_object")

        meta_refresh_tag_list = html_file_bs_object.find_all("meta", attrs = {"http-equiv" : lambda x : x and x.lower() == "refresh"})

        if not meta_refresh_tag_list :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Not Exist Meta Refresh."
            self.module_result_data["reason_data"] = ""

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        for meta_refresh_tag in meta_refresh_tag_list :

            meta_refresh_tag_content = meta_refresh_tag.get("content", "")

            redirect_url = self.get_redirect_url(meta_refresh_tag_content)
            redirect_delay = self.get_redirect_delay(meta_refresh_tag_content)

            if redirect_delay > 5 :

                continue

            if redirect_url and self.is_external_url(self.input_url, redirect_url) :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Exist External URL in Meta Refresh."
                self.module_result_data["reason_data"] = redirect_url

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Not Exist External URL in Meta Refresh."
        self.module_result_data["reason_data"] = ""

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_meta_refresh.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlMetaRefresh(input_url)

    module_instance.scan()
