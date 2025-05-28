# [ Kernel ] Module - URL : url_sub_domain.py

from kernel.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import tldextract

class UrlSubDomain(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.white_list_domain_suffix = self.get_kernel_resource("white_list_domain_suffix")
        self.white_list_brand = self.get_kernel_resource("white_list_brand")
    
    """
    IN : 
    OUT : 
    """
    async def scan(self) :
        # import time

        # time.sleep(15)

        urlparse_result = urlparse(self.input_url)

        hostname = urlparse_result.hostname
        path = urlparse_result.path

        # Run Fail Case #1
        if hostname is None :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get Host Name."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        tldextract_result = tldextract.extract(hostname)

        subdomain = tldextract_result.subdomain
        domain = tldextract_result.domain
        suffix = tldextract_result.suffix

        input_domain_suffix = f"{domain}.{suffix}"

        # print(f"[ DEBUG ] Sub Domain : {subdomain}")
        # print(f"[ DEBUG ] Domain : {domain}")
        # print(f"[ DEBUG ] Suffix : {suffix}")

        # print(f"[ DEBUG ] Domain : {input_domain_suffix}")

        # [ 1-1. ] Not Exist "input_domain_suffix" in "White List : Domain + Suffix"
        if input_domain_suffix not in self.white_list_domain_suffix :

            # print(f"[ DEBUG ] White List Domain + Suffix : {self.white_list_domain_suffix}")
            # print(f"[ DEBUG ] White List Brand : {self.white_list_brand}")

            for brand_element in self.white_list_brand :

                brand = brand_element.get("brand")

                # print(f"[ DEBUG ] ( White List ) Brand : {brand}")
                
                # [ 2-1. ] Exist "White List : Brand" in "Sub Domain" => ( Run : True ) + ( Scan : True )
                if brand in subdomain :

                    self.module_run = True
                    self.module_error = None
                    self.module_result_flag = True
                    self.module_result_data["reason"] = "Exist White List Brand in Sub Domain."
                    self.module_result_data["reason_data"] = brand

                    self.create_module_result()

                    # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                    return self.module_result_dictionary
            
                # [ 2-2. ] Not Exist "White List : Brand" in "Sub Domain"
                else :

                    # [ 3-1. ] Exist "White List : Brand" in "Path" => ( Run : True ) + ( Scan : True )
                    if brand in path :

                        self.module_run = True
                        self.module_error = None
                        self.module_result_flag = True
                        self.module_result_data["reason"] = "Exist White List Brand in Path."
                        self.module_result_data["reason_data"] = brand

                        self.create_module_result()

                        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                        return self.module_result_dictionary
                    
                    # [ 3-2. ] Not Exist "White List : Brand" in "Path" => ( Run : True ) + ( Scan : False )
                    else :

                        self.module_run = True
                        self.module_error = None
                        self.module_result_flag = False
                        self.module_result_data["reason"] = "Not Exist White List Brand in Sub Domain and Path."
                        self.module_result_data["reason_data"] = None
        
        # [ 1-2. ] Exist "input_domain_suffix" in "White List : Domain + Suffix" => ( Run : True ) + ( Scan : False )
        else :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = False
            self.module_result_data["reason"] = "Exist \"Domain + Suffix\" in White List."
            self.module_result_data["reason_data"] = None
        
        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 url_sub_domain.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = UrlSubDomain(input_url)
    
    module_instance.scan()
