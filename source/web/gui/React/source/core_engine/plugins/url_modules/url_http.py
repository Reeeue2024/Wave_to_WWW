# [ Core ] Module - URL : url_http.py

from plugins._base_module import BaseModule

import sys
import requests
from urllib.parse import urlparse

class UrlHttp(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

    """
    IN : 
    OUT : 
    """
    def get_url_protocol(self, domain) :
        try :
            response = requests.head(f"https://{domain}", timeout = 2)

            if response.status_code < 400 :

                return "https" + self.input_url[4:] if self.input_url.startswith("http://") else self.input_url

        except :
            pass

        try :
            response = requests.head(f"http://{domain}", timeout = 2)

            if response.status_code < 400 :

                return "http" + self.input_url[4:] if self.input_url.startswith("https://") else self.input_url
        
        except :
            pass

        return None

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        urlparse_result = urlparse(self.input_url)
        hostname = urlparse_result.hostname

        if not hostname :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Fail to Get Hostname."

            self.create_module_result()

            return self.module_result_dictionary

        url_with_protocol = self.get_url_protocol(hostname)

        if url_with_protocol and url_with_protocol.startswith("http://") :

            self.module_result_flag = True
            self.module_result_data["url_protocol"] = "http"
            self.module_result_data["url"] = url_with_protocol
            self.module_result_data["reason"] = "Service is HTTP."

        elif url_with_protocol and url_with_protocol.startswith("https://") :

            self.module_result_flag = False
            self.module_result_data["url_protocol"] = "https"
            self.module_result_data["url"] = url_with_protocol
            self.module_result_data["reason"] = "Service is HTTPS."

        else :

            self.module_result_flag = False
            self.module_result_data["url_protocol"] = None
            self.module_result_data["url"] = self.input_url
            self.module_result_data["reason"] = "Service is Not HTTP and HTTPS."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 url_http.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = UrlHttp(input_url)
    
    module_instance.scan()
