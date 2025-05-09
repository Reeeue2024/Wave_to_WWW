# [ Core ] Module - HTML : html_meta_refresh.py

# Tag - Meta ( Refresh )

from plugins._base_module import BaseModule

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
    def is_external_domain(self, base_url, input_url) :
        base_domain = self.get_domain_suffix(base_url)

        input_url_full = urljoin(base_url, input_url)

        input_domain = self.get_domain_suffix(input_url_full)

        return base_domain != input_domain

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
        headers = {
            "User-Agent" : "Mozilla/5.0"
        }

        try :
            response = requests.get(self.input_url, headers = headers, timeout = 5)

            response.raise_for_status()

            html = response.text

        except requests.RequestException :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Fail to Get HTML."

            self.create_module_result()

            return self.module_result_dictionary

        bs = BeautifulSoup(html, "html.parser")

        base_url = self.input_url

        meta_refresh_tag_list = bs.find_all("meta", attrs = {"http-equiv" : lambda x : x and x.lower() == "refresh"})

        if not meta_refresh_tag_list :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Meta Refresh Not Exist."

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        for meta_refresh_tag in meta_refresh_tag_list :

            meta_refresh_tag_content = meta_refresh_tag.get("content", "")

            redirect_url = self.get_redirect_url(meta_refresh_tag_content)
            redirect_delay = self.get_redirect_delay(meta_refresh_tag_content)

            if redirect_delay > 5 :

                continue

            if redirect_url and self.is_external_domain(base_url, redirect_url) :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Meta Refresh Exist. External."
                self.module_result_data["redirect_url"] = redirect_url
                self.module_result_data["redirect_delay"] = redirect_delay

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Meta Refresh Exist. Not External."
        self.module_result_data["redirect_url"] = redirect_url
        self.module_result_data["redirect_delay"] = redirect_delay

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
