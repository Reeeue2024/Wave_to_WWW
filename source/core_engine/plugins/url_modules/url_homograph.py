# [ URL Modules ] Homograph

import os
import sys
from urllib.parse import urlparse

"""
IN : URL
OUT : Scan Result ( True : Phishing O / False : Phishing X )
"""
class Homograph :
    """
    IN : 
    OUT : 
    """
    def __init__(self, input_url) :
        self.input_url = input_url
    
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
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan(self) :
        # print("Module Start.\n")

        flag = False

        # print(f"[ DEBUG ] Input URL : {self.input_url.encode()}")

        urlparse_result = urlparse(self.input_url)
        hostname = urlparse_result.hostname

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
                return
            else :
                # print("[ ✅ OK ]")
                return
        else :
            # print("[ ✅ OK ]")
            return

        # print("\nModule End.")

# Module Main
if __name__ == "__main__" :
    # Input : URL
    if len(sys.argv) != 2 :
        print("How to Use : python3 url_homograph.py < URL >")
        sys.exit(1)
    
    input_url = sys.argv[1]
    homograph = Homograph(input_url)
    homograph.scan()
