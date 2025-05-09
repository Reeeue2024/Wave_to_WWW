# [ Core ] Module - URL : url_tiny_domain.py

from plugins._base_module import BaseModule

import sys
import re
import requests

class UrlTinyDomain(BaseModule) :
    def __init__(self, input_url) :

        super().__init__(input_url)

        self.tiny_domain_list = self.get_kernel_resource("tiny_domain_list")

        self.redirect_url = None
    
    """
    IN : 
    OUT : 
    """
    def scan_tiny_domain(self) :
        # print(f"[ DEBUG ] Tiny Domain List : {self.tiny_domain_list}")

        for tiny_domain_element in self.tiny_domain_list :

            tiny_domain = tiny_domain_element.get("tiny_domain")

            # print(f"[ DEBUG ] Tiny Domain : {tiny_domain}")

            if not tiny_domain :

                continue

            pattern = rf"^https?://(www\.)?{re.escape(tiny_domain)}(/.*)?$"

            if re.search(pattern, self.input_url) :
                
                return True, tiny_domain

        return False, ""
    
    """
    IN : 
    OUT : 
    """
    def get_redirect_url(self) :
        try :
            response = requests.get(self.input_url, allow_redirects = True, timeout = 5)
            
            self.redirect_url = response.url

        except requests.RequestException :
            self.redirect_url = None

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        tiny_domain_flag, tiny_domain = self.scan_tiny_domain()

        if tiny_domain_flag :

            self.get_redirect_url()

            self.module_result_flag = True
            self.module_result_data["tiny_domain"] = tiny_domain
            self.module_result_data["redirect_url"] = self.redirect_url

        else :

            self.module_result_flag = False
            self.module_result_data["tiny_domain"] = ""
            self.module_result_data["redirect_url"] = self.input_url

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 url_tiny_domain.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = UrlTinyDomain(input_url)
    
    module_instance.scan()
