# [ Kernel ] Module - URL : url_homograph.py

from core_engine.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import subprocess
import json

class UrlHomograph(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.white_list_domain_suffix = self.get_kernel_resource("white_list_domain_suffix")

    """
    IN : 
    OUT : 
    """
    def scan_hostname_ascii(self, hostname) :
        if not hostname.isascii() :

            return True
        
        return False

    """
    IN : 
    OUT : 
    """
    def scan_hostname_punycode(self, hostname) :
        try :
            punycode = hostname.encode("idna").decode("ascii")

            if "xn--" in punycode :

                return True, punycode
            
            else :

                return False, punycode
            
        except UnicodeError :
            self.module_result_data["ERROR"] = "Fail to Encode / Decode Punycode."

            return False, None

    """
    IN : 
    OUT : 
    """
    def run_dnstwist(self, domain) :
        domain_list_open = [] # ( IPV4 / IPV6 : True )
        domain_list_close = [] # ( IPV4 / IPV6 : False ) + ( Name Server / Mail Server : True ) 

        try :
            dnstwist_result = subprocess.run(
                ["python3", "core_engine/Tools/dnstwist/dnstwist.py", "--format", "json", domain],
                capture_output=True,
                text=True,
                check=True
            )

            # print(f"[ DEBUG ] {dnstwist_result.stdout}")

            dnstwist_result_domain_list = json.loads(dnstwist_result.stdout)
            dnstwist_result_domain_list = [item for item in dnstwist_result_domain_list if item["fuzzer"] != "*original"]

            for item in dnstwist_result_domain_list :

                # ( IPV4 : True )
                if "dns_a" in item and "!ServFail" not in item["dns_a"] :
                    domain_list_open.append(item)

                # ( IPV6 : True )
                elif "dns_aaaa" in item and "!ServFail" not in item["dns_aaaa"] :
                    domain_list_open.append(item)

                # ( IPV4 / IPV6 : False ) + ( Name Server : True ) 
                elif "dns_ns" in item and "!ServFail" not in item["dns_ns"] :
                    domain_list_close.append(item)

                # ( IPV4 / IPV6 : False ) + ( Mail Server : True )
                elif "dns_mx" in item and "!ServFail" not in item["dns_mx"] :
                    domain_list_close.append(item)

        except Exception as e :
                print(f"[ ERROR ] Fail to Run \"dnstwist\" : {e}")
        
        return domain_list_open, domain_list_close

    """
    IN : 
    OUT : 
    """
    def scan_tools_dnstwist(self, hostname) :
        domain_list_open, domain_list_close = self.run_dnstwist(hostname)

        # print(f"[ DEBUG ] Number of Open : {len(domain_list_open)}")
        # print(f"[ DEBUG ] Number of Close : {len(domain_list_close)}")

        white_list_set = set(
            item.get("domain_suffix") for item in self.white_list_domain_suffix if item.get("domain_suffix")
        )

        for domain_element in domain_list_open :
            
            # print(domain_element)

            if domain_element["domain"] in white_list_set :

                # print(f"[ DEBUG ] Domain Element : {domain_element["domain"]}")

                return True, domain_element
        
        for domain_element in domain_list_close :
                    
                    # print(domain_element)

                    if domain_element["domain"] in white_list_set :

                        # print(f"[ DEBUG ] Domain Element : {domain_element["domain"]}")

                        return True, domain_element

        return False, None
                    
    """
    IN : 
    OUT : 
    """
    def scan(self) :
        urlparse_result = urlparse(self.input_url)
        hostname = urlparse_result.hostname

        if hostname is None :

            self.module_result_flag = False
            self.module_result_data["ERROR"] = "Fail to Get Host Name."

            self.create_module_result()

            return self.module_result_dictionary

        # [ 1. ] ASCII

        ascii_flag = self.scan_hostname_ascii(hostname)
        
        if ascii_flag :

            # [ 2. ] Punycode

            punycode_flag, punycode_data = self.scan_hostname_punycode(hostname)

            if punycode_flag :
                
                self.module_result_flag = True
                self.module_result_data["reason"] = "Exist Punycode in Host Name."
                self.module_result_data["reason_data"] = punycode_data

                self.create_module_result()

                return self.module_result_dictionary
        
        # [ 3. ] "dnstwist"

        dnstwist_flag, dnstwist_data = self.scan_tools_dnstwist(hostname)
        self.module_result_data["dnstwist"] = dnstwist_data

        if dnstwist_flag :

            self.module_result_flag = True
            self.module_result_data["reason"] = "Exist White List in \"dnstwist\" Result."
            self.module_result_data["reason_data"] = dnstwist_data
        
        else :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Not Exist Punycode in Host Name. / Not Exist White List in \"dnstwist\" Result."
            self.module_result_data["reason_data"] = dnstwist_data
        
        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 url_homograph.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = UrlHomograph(input_url)
    
    module_instance.scan()
