# [ URL Modules ] WHOIS

import os
import sys
from urllib.parse import urlparse
import whois
from datetime import datetime, timedelta

"""
IN : URL
OUT : Scan Result ( True : Phishing O / False : Phishing X )
"""
class UrlWhois :
    """
    IN : 
    OUT : 
    """
    def __init__(self, input_url) :
        self.input_url = input_url

        self.hostname = None
        self.whois_data = None

    """
    IN : 
    OUT : 
    """
    def get_whois_data(self) :
        try :
            self.whois_data = whois.whois(self.hostname)
            return True

        except Exception as e :
            print(f"[ ERROR ] Fail to Get \"WHOIS Data\" : {e}")
            return False
    
    """
    [ # 1 ]
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan_create_date(self, days=30) :
        creation_date = self.whois_data.creation_date

        if isinstance(creation_date, list) :
            creation_date = creation_date[0]
        
        if creation_date and isinstance(creation_date, datetime) :
            date_result = datetime.now() - creation_date

            if date_result < timedelta(days=days) :
                print(f"[ DEBUG ] Create Date : {creation_date}")
                return True
        
        return False

    """
    [ # 2 ]
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan_private_information(self) :
        fields = [
            str(self.whois_data.get("registrant_name", "")).lower(),
            str(self.whois_data.get("emails", "")).lower(),
            str(self.whois_data.get("org", "")).lower(),
        ]

        for field in fields :

            if any(keyword in field for keyword in ["privacy", "redacted", "private", "whoisguard"]):
                print(f"[ DEBUG ] Registrant Name : {fields[0]}")
                print(f"[ DEBUG ] E - Mail : {fields[1]}")
                print(f"[ DEBUG ] Organization : {fields[2]}")
                return True
        
        return False

    """
    [ # 3 ]
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan_free_tld(self) :
        free_tld_list = ["tk", "ml", "ga", "cf", "gq", "xyz"]

        if self.hostname :
            domain_data = self.hostname.split(".")
            tld_data = domain_data[-1]

            if tld_data in free_tld_list :
                print(f"[ DEBUG ] TLD : {tld_data}")
                return True

        return False

    """
    [ # 4 ]
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan_country_tld(self) :
        tld_data = self.hostname.split(".")[-1].lower()

        whois_country = str(self.whois_data.get("country", "")).lower()

        country_tld_map = {
            "ru" : "ru",
            "cn" : "cn",
            "kr" : "kr",
            "jp" : "jp",
            "ir" : "ir"
        }

        if whois_country :

            if tld_data in country_tld_map and not whois_country.endswith(country_tld_map[tld_data]) :
                print(f"[ DEBUG ] TLD Country : {tld_data}")
                print(f"[ DEBUG ] \"WHOIS\" Country : {whois_country}")
                return True
            
        else :
            return False

    """
    IN : 
    OUT : True ( Suspicious ) / False ( OK )
    """
    def scan(self) :
        # print("Module Start.\n")

        urlparse_result = urlparse(self.input_url)
        self.hostname = urlparse_result.hostname

        self.get_whois_data()

        # print("[ DEBUG ] \"WHOIS Data\"")
        # print(f"{self.whois_data}")

        if not self.hostname :
            print("* * * * * * * * * *")
            print("[ ERROR ] Can't Get \"Host Name\" from Input URL.")
            print(f">>>> Input URL : {self.input_url}")
            print("* * * * * * * * * *")
            # sys.exit(1)
            return # ( For TEST ) To-Do

        if not self.whois_data :
            print("* * * * * * * * * *")
            print("[ ERROR ] Can't Get \"WHOIS Data\" from Input URL.")
            print(f">>>> Input URL : {self.input_url}")
            print("* * * * * * * * * *")
            # sys.exit(1)
            return # ( For TEST ) To-Do

        scan_result_list = []

        if self.scan_create_date() :
            scan_result_list.append("create_date")

        if self.scan_private_information() :
            scan_result_list.append("private_information")

        if self.scan_free_tld() :
            scan_result_list.append("free_tld")

        if self.scan_country_tld() :
            scan_result_list.append("country_tld")

        if scan_result_list :
            print("[ ⚠️ Suspicious ⚠️ ]")
            print(f">>>> Input URL : {self.input_url}")
            print(f">>>> Result : {" / ".join(scan_result_list)}")
            return True
        
        else :
            print("[ ✅ OK ]")
            return False
        
        # print("\nModule End.")

# Module Main
if __name__ == "__main__" :
    # Input : URL
    if len(sys.argv) != 2 :
        print("How to Use : python3 url_whois.py < URL >")
        sys.exit(1)
    
    input_url = sys.argv[1]
    whois_instance = UrlWhois(input_url)
    whois_instance.scan()
