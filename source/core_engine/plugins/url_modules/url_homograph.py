# [ Kernel ] Module - URL : url_homograph.py

from core_engine.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import json
import asyncio

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

                return True, punycode, False
            
            else :

                return False, punycode, False
            
        except UnicodeError :
            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Encode / Decode Punycode."
            self.module_result_flag = False
            self.module_result_data = None

            return False, None, True

    """
    IN : 
    OUT : 
    """
    async def run_dnstwist(self, domain) :
        domain_list_open = [] # ( IPV4 / IPV6 : True )
        domain_list_close = [] # ( IPV4 / IPV6 : False ) + ( Name Server / Mail Server : True ) 

        try :
            # [ 1. ] Create Asynchronous Process - "dnstwist"
            process = await asyncio.create_subprocess_exec(
                "python3", "core_engine/tools/dnstwist/dnstwist.py", "--format", "json", domain,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            # [ 2. ] Get "Time-Out" From Engine
            time_out = getattr(self, "time_out_module", 30)

            # [ 3. ] Set "Time-Out"
            try :
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout = time_out)

            except asyncio.TimeoutError :
                process.kill()

                await process.communicate()

                self.module_run = False
                self.module_error = f"[ ERROR ] TIME OUT : {time_out}"
                self.module_result_flag = False
                self.module_result_data = None

                return domain_list_open, domain_list_close, True
            
            dnstwist_result_domain_list = json.loads(stdout.decode())
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
            self.module_run = False
            self.module_error = f"[ ERROR ] {e}"
            self.module_result_flag = False
            self.module_result_data = None

            return domain_list_open, domain_list_close, True
        
        return domain_list_open, domain_list_close, False

    """
    IN : 
    OUT : 
    """
    async def scan_tools_dnstwist(self, hostname) :
        domain_list_open, domain_list_close, dnstwist_error_flag = await self.run_dnstwist(hostname)

        # print(f"[ DEBUG ] Number of Open : {len(domain_list_open)}")
        # print(f"[ DEBUG ] Number of Close : {len(domain_list_close)}")

        white_list_set = set(
            item.get("domain_suffix") for item in self.white_list_domain_suffix if item.get("domain_suffix")
        )

        for domain_element in domain_list_open :
            
            # print(domain_element)

            if domain_element["domain"] in white_list_set :

                # print(f"[ DEBUG ] Domain Element : {domain_element["domain"]}")

                return True, domain_element, dnstwist_error_flag
        
        for domain_element in domain_list_close :
                    
                    # print(domain_element)

                    if domain_element["domain"] in white_list_set :

                        # print(f"[ DEBUG ] Domain Element : {domain_element["domain"]}")

                        return True, domain_element, dnstwist_error_flag

        return False, None, dnstwist_error_flag
                    
    """
    IN : 
    OUT : 
    """
    async def scan(self) :
        urlparse_result = urlparse(self.input_url)
        hostname = urlparse_result.hostname

        # Run Fail Case #1
        if hostname is None :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get Host Name."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        # [ 1. ] ASCII

        ascii_flag = self.scan_hostname_ascii(hostname)
        
        if ascii_flag :

            # [ 2. ] Punycode

            punycode_flag, punycode_data, punycode_error_flag = self.scan_hostname_punycode(hostname)

            # Run Fail Case #2
            if punycode_error_flag :

                self.create_module_result()

                return self.module_result_dictionary

            # ( Run : True ) + ( Scan : True )
            if punycode_flag :
                
                self.module_run = True
                self.module_error = None
                self.module_result_flag = True
                self.module_result_data["reason"] = "Exist Punycode in Host Name."
                self.module_result_data["reason_data"] = punycode_data

                self.create_module_result()

                return self.module_result_dictionary
        
        # [ 3. ] "dnstwist"

        dnstwist_flag, dnstwist_data, dnstwist_error_flag = await self.scan_tools_dnstwist(hostname)

        # Run Fail Case #3
        if dnstwist_error_flag :

            self.create_module_result()

            return self.module_result_dictionary

        # ( Run : True ) + ( Scan : True )
        if dnstwist_flag :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = True
            self.module_result_data["reason"] = "Exist White List in \"dnstwist\" Result."
            self.module_result_data["reason_data"] = dnstwist_data
        
        # ( Run : True ) + ( Scan : False )
        else :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = False
            self.module_result_data["reason"] = "Not Exist Punycode in Host Name. / Not Exist White List in \"dnstwist\" Result."
            self.module_result_data["reason_data"] = None
        
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
