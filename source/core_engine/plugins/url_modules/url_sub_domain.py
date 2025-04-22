# [ URL Modules ] Sub Domain

import os
import sys
from urllib.parse import urlparse
import tldextract

"""
IN : URL
OUT : Scan Result ( True : Phishing O / False : Phishing X )
"""
class UrlSubDomain :
    # [ Class Level ] White List : Domain + Suffix
    white_list_domain_suffix = None
    # [ Class Level ] White List : Brand => To-Do
    white_list_brand = [
        "google", "paypal", "apple", "microsoft", "naver", "kakao"
    ]

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
    def scan(self) :
        # print("Module Start.\n")

        flag = False

        urlparse_result = urlparse(self.input_url)
        hostname = urlparse_result.hostname
        path = urlparse_result.path

        if hostname is None :
            print("* * * * * * * * * *")
            print("[ ERROR ] Can't Get \"Host Name\" from Input URL.")
            print(f">>>> Input URL : {self.input_url}")
            print("* * * * * * * * * *")
            # sys.exit(1)
            return # ( For TEST ) To-Do
                
        print(f"[ DEBUG ] Host Name : {hostname}")
        print(f"[ DEBUG ] Path : {path}")

        tldextract_result = tldextract.extract(hostname)

        subdomain = tldextract_result.subdomain
        domain = tldextract_result.domain
        suffix = tldextract_result.suffix

        input_domain_suffix = f"{domain}.{suffix}"

        print(f"[ DEBUG ] Sub Domain : {subdomain}")
        print(f"[ DEBUG ] Domain : {domain}")
        print(f"[ DEBUG ] Suffix : {suffix}")

        print(f"[ DEBUG ] Domain : {input_domain_suffix}")

        # ( 1-1 ) "White List : Domain + Suffix"에 "input_domain_suffix" 없을 경우
        if input_domain_suffix not in self.white_list_domain_suffix :
            for brand in self.white_list_brand :
                # ( 2-1 ) 하지만 "Sub Domain"에 "White List : Brand" 있을 경우 => "Suspicious"
                if brand in subdomain :
                    print(f"[ ⚠️ Suspicious ]")
                    print(f">>>> ( Suspicious ) Brand : \"{brand}\"")
                    print(f">>>> ( Suspicious ) Sub Domain : {subdomain}")
                    print(f">>>> Domain + Suffix : {input_domain_suffix}")
                    print(f">>>> Input URL : {self.input_url}")
                    return True
            
                # ( 2-2 ) 그리고 "Sub Domain"에 "White List : Brand" 없을 경우
                else :
                    # ( 3-1 ) 하지만 "Path"에 "White List : Brand" 있을 경우 => "Suspicious"
                    if brand in path :
                        print(f"[ ⚠️ Suspicious ]")
                        print(f">>>> ( Suspicious ) Brand : \"{brand}\"")
                        print(f">>>> ( Suspicious ) Path : {path}")
                        print(f">>>> Domain + Suffix : {input_domain_suffix}")
                        print(f">>>> Input URL : {self.input_url}")
                        return True
                    
                    # ( 3-2 ) 그리고 "Path"에 "White List : Brand" 없을 경우 => "OK"
                    else :
                        print(f"[ OK - DEBUG ] N IN - White List : Brand")
                        print(f"[ ✅ OK ]")
                        return False
        
        # ( 1-2 ) "White List : Domain + Suffix"에 "input_domain_suffix" 있을 경우 => "OK"
        else :
            print(f"[ OK - DEBUG ] IN - White List : Domain + Suffix")
            print(f"[ ✅ OK ]")
            return False
        
        # print("\nModule End.")

# Module Main
if __name__ == "__main__" :
    # Input : URL
    if len(sys.argv) != 2 :
        print("How to Use : python3 url_sub_domain.py < URL >")
        sys.exit(1)
    
    input_url = sys.argv[1]
    sub_domain_instance = UrlSubDomain(input_url)
    sub_domain_instance.scan()
