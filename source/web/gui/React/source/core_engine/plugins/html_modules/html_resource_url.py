# [ Core ] Module - HTML : html_resource_url.py

# Tag - Link / Script / Image

from plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract

class HtmlResourceUrl(BaseModule) :
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
    def scan(self) :
        headers = {
            "User-Agent" : "Mozilla/5.0"
        }

        try :
            response = requests.get(self.input_url, headers = headers, timeout = 5, allow_redirects = True)

            response.raise_for_status()

            html = response.text

        except requests.RequestException as e :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Fail to Get HTML."

            self.create_module_result()

            return self.module_result_dictionary

        bs = BeautifulSoup(html, "html.parser")

        base_url = self.input_url

        resource_url_list = []

        # [ 1. ] Link
        for tag in bs.find_all("link", href = True) :
            resource_url_list.append(tag["href"])

        # [ 2. ] Script
        for tag in bs.find_all("script", src = True) :
            resource_url_list.append(tag["src"])

        # [ 3. ] Image
        for tag in bs.find_all("img", src = True) :
            resource_url_list.append(tag["src"])

        if not resource_url_list :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Resource URL Not Exist."

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        for resource_url in resource_url_list :

            if resource_url.startswith("http://") or self.is_external_domain(base_url, resource_url) :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Resource URL is External."
                self.module_result_data["resource_url"] = resource_url

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Resource URL is Not External."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary
    
# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_resource_url.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlResourceUrl(input_url)

    module_instance.scan()
