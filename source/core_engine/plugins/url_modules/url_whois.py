# [ Kernel ] Module - URL : url_whois.py

from core_engine.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
from datetime import datetime, timedelta
import whois

class UrlWhois(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.free_tld_list = self.get_kernel_resource("free_tld_list")
        self.country_tld_list = self.get_kernel_resource("country_tld_list")

        self.hostname = urlparse(self.input_url).hostname

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

                return True, creation_date
        
        return False, creation_date

    """
    IN : 
    OUT : 
    """
    def scan_private_information(self) :
        field_list = [
            str(self.whois_data.get("registrant_name", "")).lower(),
            str(self.whois_data.get("emails", "")).lower(),
            str(self.whois_data.get("org", "")).lower(),
        ]

        for field in field_list :

            if any(keyword in field for keyword in ["privacy", "redacted", "private", "whoisguard"]) :

                return True, field

        return False, field

    """
    IN : 
    OUT : 
    """
    def scan_free_tld(self) :
        if self.hostname :

            tld = self.hostname.split(".")[-1].lower()

            if tld in self.free_tld_list :

                return True, tld

        return False, tld

    """
    IN : 
    OUT : 
    """
    def scan_tld_whois_country(self) :
        tld = self.hostname.split(".")[-1].lower()
        country_from_whois = str(self.whois_data.get("country", "")).lower()

        if tld in self.country_tld_list :

            country_from_whois = str(self.whois_data.get("country", "")).lower()

            if tld not in country_from_whois:

                return True, country_from_whois
        
        return False, country_from_whois

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        if self.hostname is None :

            self.module_result_flag = False
            self.module_result_data["ERROR"] = "Fail to Get Host Name."

            self.create_module_result()

            return self.module_result_dictionary
        
        whois_flag = self.get_whois_data()

        if not whois_flag :
            
            self.module_result_flag = False
            self.module_result_data["ERROR"] = "Fail to Get WHOIS Data."

            self.create_module_result()

            return self.module_result_dictionary

        reason_list = []

        # [ 1. ] Create Date
        create_date_flag, create_date_data = self.scan_create_date()

        if create_date_flag :

            reason_dictionary = {}

            reason_dictionary["reason"] = "Create Date is Recent."
            reason_dictionary["reason_data"] = create_date_data

            reason_list.append(reason_dictionary)

        # [ 2. ] Private Information
        private_information_flag, private_information_data = self.scan_private_information()

        if private_information_flag :

            reason_dictionary = {}

            reason_dictionary["reason"] = "Use Private Information."
            reason_dictionary["reason_data"] = private_information_data

            reason_list.append(reason_dictionary)

        # [ 3. ] Free TLD
        free_tld_flag, free_tld_data = self.scan_free_tld()

        if free_tld_flag :

            reason_dictionary = {}

            reason_dictionary["reason"] = "Use Free TLD."
            reason_dictionary["reason_data"] = free_tld_data

            reason_list.append(reason_dictionary)

        # [ 4. ] Country
        tld_whois_country_flag, tld_whois_country_data = self.scan_tld_whois_country()

        if tld_whois_country_flag :

            reason_dictionary = {}

            reason_dictionary["reason"] = "Country ( TLD ) is Different with \"WHOIS\"."
            reason_dictionary["reason_data"] = tld_whois_country_data

            reason_list.append(reason_dictionary)

        if create_date_flag or private_information_flag or free_tld_flag or tld_whois_country_flag :

            self.module_result_flag = True
            self.module_result_data["reason"] = " / ".join([reason_element["reason"] for reason_element in reason_list])
            self.module_result_data["reason_data"] = " / ".join([str(reason_element["reason_data"]) for reason_element in reason_list])

        else :

            self.module_result_flag = False
            self.module_result_data["reason"] = ""
            self.module_result_data["reason_data"] = ""

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
