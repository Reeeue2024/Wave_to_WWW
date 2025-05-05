# [ Core ] Module - URL : url_sub_domain.py

from plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import tldextract # pip install tldextract

class UrlSubDomain(BaseModule) :
    def __init__(self, input_url) :

        super().__init__(input_url)

        self.white_list_domain_suffix = self.get_kernel_resource("white_list_domain_suffix")
        self.white_list_brand = self.get_kernel_resource("white_list_brand")
    
    """
    IN : 
    OUT : 
    """
    def scan(self) :
        urlparse_result = urlparse(self.input_url)
        hostname = urlparse_result.hostname
        path = urlparse_result.path

        if hostname is None :

            self.module_result_flag = False
            self.module_result_data["error"] = "Fail to Get Hostname."

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

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

        # [ 1-1. ] "White List : Domain + Suffix"에 "input_domain_suffix" 없을 경우
        if input_domain_suffix not in self.white_list_domain_suffix :

            # print(f"[ DEBUG ] White List Domain + Suffix : {self.white_list_domain_suffix}")
            # print(f"[ DEBUG ] White List Brand : {self.white_list_brand}")

            for brand_element in self.white_list_brand :

                brand = brand_element.get("brand")

                # print(f"[ DEBUG ] ( White List ) Brand : {brand}")
                
                # [ 2-1. ] 하지만 "Sub Domain"에 "White List : Brand" 있을 경우 => True
                if brand in subdomain :

                    self.module_result_flag = True
                    self.module_result_data["reason"] = f"Brand in Sub Domain. ( {brand} )"

                    self.create_module_result()

                    # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                    return self.module_result_dictionary
            
                # [ 2-2. ] 그리고 "Sub Domain"에 "White List : Brand" 없을 경우
                else :

                    # [ 3-1. ] 하지만 "Path"에 "White List : Brand" 있을 경우 => True
                    if brand in path :

                        self.module_result_flag = True
                        self.module_result_data["reason"] = f"Brand in Path. ( {brand} )"

                        self.create_module_result()

                        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                        return self.module_result_dictionary
                    
                    # [ 3-2. ] 그리고 "Path"에 "White List : Brand" 없을 경우 => False
                    else :

                        self.module_result_flag = False
                        self.module_result_data["reason"] = "Brand Not in Sub Domain and Path."
        
        # [ 1-2. ] "White List : Domain + Suffix"에 "input_domain_suffix" 있을 경우 => False
        else :
            self.module_result_flag = False
            self.module_result_data["reason"] = "Domain + Suffix in White List."
        
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
