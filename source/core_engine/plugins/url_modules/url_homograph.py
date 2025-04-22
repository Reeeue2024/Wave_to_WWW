# [ URL Modules ] Homograph

import os
import sys
from urllib.parse import urlparse
import subprocess
import json

"""
IN : URL
OUT : Scan Result ( True : Phishing O / False : Phishing X )
"""
class UrlHomograph :
    # [ Class Level ] White List : Domain + Suffix => To-Do
    white_list_domain_suffix = [ "google.com", "paypal.com", "apple.com", "microsoft.com", "naver.com", "kakao.com" ]
    
    """
    IN : 
    OUT : 
    """
    def __init__(self, input_url) :
        self.input_url = input_url

        self.load_white_lists()
    
    """
    IN : 
    OUT : 
    """
    @classmethod
    def load_white_lists(cls) :
        if cls.white_list_domain_suffix is not None :
            return
        
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        WHITE_LIST_DOMAIN_SUFFIX_PATH = os.path.abspath(
            os.path.join(BASE_PATH, "../../_white_list/white_list_top-1m_domain.txt")
        )

        # White List : Domain + Suffix
        cls.white_list_domain_suffix = []

        try :
            with open(WHITE_LIST_DOMAIN_SUFFIX_PATH, "r", encoding="utf-8") as f :
                for line in f :
                    line = line.strip().lower()

                    if not line or line.startswith("#") :
                        continue
                    
                    cls.white_list_domain_suffix.append(line)

        except FileNotFoundError :
            print(f"[ ERROR ] Fail to Load White List File ( Domain + Suffix ) : {WHITE_LIST_DOMAIN_SUFFIX_PATH}")

    """
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan_hostname_ascii(self, hostname) :
        # 1st

        # Not Only ASCII : Suspicious
        if not hostname.isascii() :
            # print("[ 1st ] Suspicious")
            return True
        
        # Only ASCII : OK
        else :
            # print("[ 1st ] OK")
            return False

    """
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan_hostname_punycode(self, hostname) :
        # 2nd
        
        try :
            punycode = hostname.encode("idna").decode("ascii")
            # print(f"[ DEBUG ] Punycode : {punycode}")

            # Include Punycode : Suspicious
            if "xn--" in punycode :
                # print("[ 2nd ] Suspicious")
                return True
            
            # Not Include Punycode : OK
            else :
                # print("[ 2nd ] OK")
                return False
            
        except UnicodeError as e :
            print(f"[ DEBUG ] Fail to Encode Punycode ( \"idna\" ) : {e}")
            return False # To-Do
    
    """
    IN : 
    OUT : 
    """
    def scan_ascii_homograph_table(self) :
        print() # To-Do

    """
    IN : 
    OUT : 
    """
    def scan_ascii_homograph_rapidfuzz(self) :
        print() # To-Do
    
    """
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan_tools_dnstwist(self, hostname) :
        domain_list_suspicious_open, domain_list_suspicious_close = self.run_dnstwist(hostname)

        print(f"[ DEBUG ] Number of Suspicious Open : {len(domain_list_suspicious_open)}")
        # print(f"[ DEBUG ] Number of Suspicious Close : {len(domain_list_suspicious_close)}")

        for domain_element in domain_list_suspicious_open :
            # print(domain_element)

            for white_element in self.white_list_domain_suffix :
                if domain_element["domain"] == white_element :
                    return True
        
        return False
        
        # To-Do
        # for domain in domain_list_suspicious_close :
        #     print(domain)

    """
    IN : 
    OUT : 
    """
    def run_dnstwist(self, domain) :
        domain_list_suspicious_open = [] # ( IPV4 / IPV6 : True )
        domain_list_suspicious_close = [] # ( IPV4 / IPV6 : False ) + ( Name Server / Mail Server : True ) 

        try :
            dnstwist_result = subprocess.run(
                ["python3", "../../tools/dnstwist/dnstwist.py", "--format", "json", domain],
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
                    domain_list_suspicious_open.append(item)
                # ( IPV6 : True )
                elif "dns_aaaa" in item and "!ServFail" not in item["dns_aaaa"] :
                    domain_list_suspicious_open.append(item)
                # ( IPV4 / IPV6 : False ) + ( Name Server : True ) 
                elif "dns_ns" in item and "!ServFail" not in item["dns_ns"] :
                    domain_list_suspicious_close.append(item)
                # ( IPV4 / IPV6 : False ) + ( Mail Server : True )
                elif "dns_mx" in item and "!ServFail" not in item["dns_mx"] :
                    domain_list_suspicious_close.append(item)

        except Exception as e :
                print(f"[ ERROR ] Fail to Run ( Tools - \"dnstwist\" ) : {e}")
        
        return domain_list_suspicious_open, domain_list_suspicious_close
        
    """
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan(self) :
        # print("Module Start.\n")

        flag = False

        # print(f"[ DEBUG ] Input URL : {self.input_url.encode()}")

        urlparse_result = urlparse(self.input_url)
        hostname = urlparse_result.hostname

        # print(f"[ DEBUG ] Host Name : {hostname}")

        if hostname is None :
            print("* * * * * * * * * *")
            print("[ ERROR ] Can't Get \"Host Name\" from Input URL.")
            print(f">>>> Input URL : {self.input_url}")
            print("* * * * * * * * * *")
            # sys.exit(1)
            return # ( For TEST ) To-Do

        flag = self.scan_hostname_ascii(hostname)
        if flag == True :
            flag = self.scan_hostname_punycode(hostname)
            if flag == True :
                # print("[ ⚠️ Suspicious ⚠️ ]")
                # print(f">>>> Input URL : {self.input_url}")
                return True
        
        flag = self.scan_tools_dnstwist(hostname)
        if flag == True :
                # print("[ ⚠️ Suspicious ⚠️ ]")
                # print(f">>>> Input URL : {self.input_url}")
                return True
        
        # print(f"[ ✅ OK ]")
        return False

        # print("\nModule End.")

# Module Main
if __name__ == "__main__" :
    # Input : URL
    if len(sys.argv) != 2 :
        print("How to Use : python3 url_homograph.py < URL >")
        sys.exit(1)
    
    input_url = sys.argv[1]
    homograph_instance = UrlHomograph(input_url)
    homograph_instance.scan()
