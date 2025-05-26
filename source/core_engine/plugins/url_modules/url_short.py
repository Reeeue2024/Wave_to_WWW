# [ Kernel ] Module - URL : url_short.py

from core_engine.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import requests
import tldextract

class UrlShort(BaseModule) :
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
    def scan_different_domain_suffix(self, one_url, two_url) :
        one_domain_suffix = self.get_domain_suffix(one_url)
        two_domain_suffix = self.get_domain_suffix(two_url)

        return one_domain_suffix != two_domain_suffix
    
    """
    IN : 
    OUT : 
    """
    def scan_different_url(self, one_url, two_url) :
        one_domain_suffix = self.get_domain_suffix(one_url)
        two_domain_suffix = self.get_domain_suffix(two_url)

        if one_domain_suffix != two_domain_suffix :

            one_urlparse_result = urlparse(one_url)
            two_urlparse_result = urlparse(two_url)

            return (
                one_urlparse_result.path != two_urlparse_result.path or one_urlparse_result.query != two_urlparse_result.query
            )
        
        return False
    
    """
    IN : 
    OUT : 
    """
    def get_redirect_url(self) :
        try :
            headers = {
                "User-Agent" : (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
            }

            response = requests.get(self.input_url, headers = headers, allow_redirects = True, timeout = 5)

            self.redirect_url = response.url

        except requests.RequestException :
            self.redirect_url = None

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        self.get_redirect_url()

        # print(f"[ DEBUG ] Redirect URL : {self.redirect_url}")

        # Run Fail Case #1
        if self.redirect_url is None :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get Response."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        if self.input_url != self.redirect_url :

            different_url_flag = self.scan_different_url(self.input_url, self.redirect_url)

            # ( Run : True ) + ( Scan : True )
            if different_url_flag :

                self.module_run = True
                self.module_error = None
                self.module_result_flag = True
                self.module_result_data["reason"] = "Exist Short URL."
                self.module_result_data["reason_data"] = self.redirect_url

                # Engine Resource
                self.engine_resource["redirect_url"] = self.redirect_url

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        # ( Run : True ) + ( Scan : False )
        self.module_run = True
        self.module_error = None
        self.module_result_flag = False
        self.module_result_data["reason"] = "Not Exist Short URL."
        self.module_result_data["reason_data"] = None

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
