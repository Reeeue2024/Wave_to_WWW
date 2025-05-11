# [ Kernel ] Module - URL : url_short.py

from core_engine.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import requests

class UrlShort(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.short_domain_list = self.get_kernel_resource("short_domain_list")
    
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
        urlparse_result = urlparse(self.input_url)
        netloc = urlparse_result.netloc.lower()

        if netloc is None :

            self.module_result_flag = False
            self.module_result_data["ERROR"] = "Fail to Get Network Location."

            self.create_module_result()

            return self.module_result_dictionary

        if netloc.startswith("www.") :

            netloc = netloc[4:]
        
        if netloc in self.short_domain_list :

            self.get_redirect_url()
        
        if self.redirect_url is not None and self.input_url != self.redirect_url :

            self.module_result_flag = True
            self.module_result_data["reason"] = "Exist Short URL."
            self.module_result_data["reason_data"] = self.redirect_url

            self.engine_resource["redirect_url"] = self.redirect_url
        
        else :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Not Exist Short URL."
            self.module_result_data["reason_data"] = self.redirect_url

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 url_short.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = UrlShort(input_url)
    
    module_instance.scan()
