# [ URL Modules ] Sub Domain

import os
import sys
from urllib.parse import urlparse
import tldextract

"""
IN : URL
OUT : Scan Result ( True : Phishing O / False : Phishing X )
"""
class Sub_Domain :
    """
    IN : 
    OUT : 
    """
    def __init__(self, input_url) :
        self.input_url = input_url

        # To-Do
        # "OK" Domain List
        self.ok_domain_list = [
            "google.com", "paypal.com", "apple.com", "microsoft.com", "naver.com", "kakao.com"
        ]
        # To-Do
        # "OK" Keyword List
        self.ok_keyword_list = [
            "google", "paypal", "apple", "microsoft", "naver", "kakao"
        ]

    """
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan(self) :
        # print("Module Start.\n")

        flag = False

        urlparse_result = urlparse(self.input_url)
        hostname = urlparse_result.hostname

        if hostname is None :
            print("* * * * * * * * * *")
            print("[ ERROR ] Can't Get \"Host Name\" from Input URL.")
            print(f">>>> Input URL : {self.input_url}")
            print("* * * * * * * * * *")
            # sys.exit(1)
            return # ( For TEST ) To-Do
        
        # print(f"[ DEBUG ] Host Name : {hostname}")

        tldextract_result = tldextract.extract(hostname)
        subdomain = tldextract_result.subdomain
        domain = tldextract_result.domain
        suffix = tldextract_result.suffix

        input_url_domain = f"{domain}.{suffix}"

        # print(f"[ DEBUG ] Sub Domain : {subdomain}")
        # print(f"[ DEBUG ] Domain : {domain}")
        # print(f"[ DEBUG ] Suffix : {suffix}")

        # print(f"[ DEBUG ] URL Domain : {input_url_domain}")

        # 1-1. Not Exist in "OK Domain List"
        if input_url_domain not in self.ok_domain_list :
            for keyword in self.ok_keyword_list :
                # 2-1. But Exist in "OK Keyword List" => Suspicious
                if keyword in subdomain :
                    # print(f"[ ⚠️ Suspicious ]")
                    # print(f">>>> ( Suspicious ) Keyword : \"{keyword}\"")
                    # print(f">>>> Input URL : {self.input_url}")
                    return True
            
                # 2-2. And Not Exist in "OK Keyword List" => OK
                else :
                    # print(f"[ ✅ OK ]")
                    return False
        
        # 1-2. Exist in "OK Domain List"
        else :
            # print(f"[ ✅ OK ]")
            return False

        # print("\nModule End.")

# Module Main
if __name__ == "__main__" :
    # Input : URL
    if len(sys.argv) != 2 :
        print("How to Use : python3 url_sub_domain.py < URL >")
        sys.exit(1)
    
    input_url = sys.argv[1]
    sub_domain = Sub_Domain(input_url)
    sub_domain.scan()
