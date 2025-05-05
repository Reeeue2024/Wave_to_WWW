# [ Core ] Module - URL : url_whois.py

from plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
from datetime import datetime, timedelta
import whois # pip install python-whois

class UrlWhois(BaseModule) :
    def __init__(self, input_url) :

        super().__init__(input_url)

        self.hostname = urlparse(self.input_url).hostname

        self.whois_data = None

        self.free_tld_list = self.get_kernel_resource("free_tld_list")
        self.country_tld_list = self.get_kernel_resource("country_tld_list")

    """
    IN : 
    OUT : 
    """
    def get_whois_data(self) :
        try :
            self.whois_data = whois.whois(self.hostname)

            return True
        
        except Exception as e :
            return False

    """
    IN : 
    OUT : 
    """
    def scan_create_date(self, days = 30) :
        creation_date = self.whois_data.creation_date

        if isinstance(creation_date, list) :

            creation_date = creation_date[0]

        if creation_date and isinstance(creation_date, datetime) :

            date_result = datetime.now() - creation_date

            if date_result < timedelta(days = days) :

                return True, f"Recent Create Date. ( {creation_date} )"
        
        return False, "Not Recent Create Date."

    """
    IN : 
    OUT : 
    """
    def scan_private_information(self) :
        fields = [
            str(self.whois_data.get("registrant_name", "")).lower(),
            str(self.whois_data.get("emails", "")).lower(),
            str(self.whois_data.get("org", "")).lower(),
        ]

        for field in fields :

            if any(keyword in field for keyword in ["privacy", "redacted", "private", "whoisguard"]) :

                return True, "Information is Private."

        return False, "Information is Not Private."

    """
    IN : 
    OUT : 
    """
    def scan_free_tld(self) :
        if self.hostname :

            tld = self.hostname.split(".")[-1].lower()

            if tld in self.free_tld_list :

                return True, f"Free TLD. ( {tld} )"

        return False, "Not Free TLD."

    """
    IN : 
    OUT : 
    """
    def scan_tld_whois_country(self) :
        tld = self.hostname.split(".")[-1].lower()

        if tld in self.country_tld_list :

            country_from_whois = str(self.whois_data.get("country", "")).lower()

            if not country_from_whois.endswith(tld) :

                return True, f"Different TLD Country and WHOIS Country. ( TLD : .{tld} / WHOIS : {country_from_whois} )"

            return False, "Not Different TLD Country and WHOIS Country."
        
        return False, "Not TLD Country."

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        if self.hostname is None :

            self.module_result_flag = False
            self.module_result_data["error"] = "Fail to Get Hostname."

            self.create_module_result()

            return self.module_result_dictionary
        
        if not self.get_whois_data() :
            
            self.module_result_flag = False
            self.module_result_data["error"] = "Fail to Get WHOIS Data."

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        reason_list = []

        create_date_flag, create_date_data = self.scan_create_date()
        private_information_flag, private_information_data = self.scan_private_information()
        free_tld_flag, free_tld_data = self.scan_free_tld()
        tld_whois_country_flag, tld_whois_country_data = self.scan_tld_whois_country()

        self.module_result_data["create_date"] = create_date_data
        self.module_result_data["private_information"] = private_information_data
        self.module_result_data["free_tld"] = free_tld_data
        self.module_result_data["tld_whois_country"] = tld_whois_country_data

        if create_date_flag or private_information_flag or free_tld_flag or tld_whois_country_flag :

            self.module_result_flag = True

            if create_date_flag : reason_list.append("create_date")
            if private_information_flag : reason_list.append("private_information")
            if free_tld_flag : reason_list.append("free_tld")
            if tld_whois_country_flag : reason_list.append("tld_whois_country")
            
            self.module_result_data["reason"] = " / ".join(reason_list)

        else :

            self.module_result_flag = False
            self.module_result_data["reason"] = ""

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 url_whois.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = UrlWhois(input_url)

    module_instance.scan()
