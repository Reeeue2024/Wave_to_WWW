# [ Kernel ] Module - URL : url_http.py

from core_engine.plugins._base_module import BaseModule

import sys
import requests
from urllib.parse import urlparse, urlunparse

class UrlHttp(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

    """
    IN : 
    OUT : 
    """
    def get_url_protocol(self) :
        if "://" not in self.input_url :

            self.input_url = "http://" + self.input_url

        urlparse_result = urlparse(self.input_url)
        netloc = urlparse_result.netloc
        path = urlparse_result.path
        params = urlparse_result.params
        query = urlparse_result.query
        fragment = urlparse_result.fragment

        # [ 1. ] HTTPS
        try :
            url = urlunparse(("http", netloc, path, params, query, fragment))

            response = requests.head(url, timeout = 2, allow_redirects = True)

            if response.status_code < 400 :
                
                return url
        except requests.RequestException :
            pass

        # [ 2. ] HTTP
        try :
            url = urlunparse(("https", netloc, path, params, query, fragment))

            response = requests.head(url, timeout = 2, allow_redirects = True)

            if response.status_code < 400 :
                
                return url
        except requests.RequestException :
            pass

        return None

    """
    IN : 
    OUT : 
    """
    async def scan(self) :
        url_with_protocol = self.get_url_protocol()

        # Run Fail Case #1
        if url_with_protocol is None :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get HTTP / HTTPS Protocol."
            self.module_result_flag = False
            self.module_result_data = None

        # ( Run : True ) + ( Scan : True )
        elif url_with_protocol.startswith("http://") :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = True
            self.module_result_data["reason"] = "Use HTTP."
            self.module_result_data["reason_data"] = url_with_protocol

        # ( Run : True ) + ( Scan : False )
        elif url_with_protocol.startswith("https://") :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = False
            self.module_result_data["reason"] = "Use HTTPS."
            self.module_result_data["reason_data"] = None

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
