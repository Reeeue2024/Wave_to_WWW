# [ Kernel ] Module - HTML : html_form.py

from core_engine.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import tldextract

class HtmlForm(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.m_form_list = []

    """
    IN : 
    OUT : 
    """
    def get_domain_suffix(self, url) :
        tldextract_result = tldextract.extract(url)

        return f"{tldextract_result.domain}.{tldextract_result.suffix}"

    """
    IN : 
    OUT : 
    """
    def is_external_url(self, one_url, two_url) :
        one_domain_suffix = self.get_domain_suffix(one_url)
        two_domain_suffix = self.get_domain_suffix(two_url)

        return one_domain_suffix != two_domain_suffix

    """
    IN : 
    OUT : 
    """
    async def scan(self) :
        html_file_bs_object = self.engine_resource.get("html_file_bs_object")

        # Run Fail Case #1
        if not html_file_bs_object :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get HTML File from Engine."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        form_list = html_file_bs_object.find_all("form")

        # Run Fail Case #2
        if not form_list :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get \"form\" Tag from HTML File."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary   

        reason_list = []
        reason_data_list = []

        external_url_flag = False

        for form in form_list :

            form_action_data = form.get("action", "")

            external_url_flag = self.is_external_url(self.input_url, form_action_data)

            if external_url_flag :

                reason_list.append("Exist External URL in \"form\" Tag.")
                reason_data_list.append(form_action_data)
            
            else :

                continue
        
        # ( Run : True ) + ( Scan : True )
        if reason_list or reason_data_list :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = True
            self.module_result_data["reason"] = reason_list
            self.module_result_data["reason_data"] = reason_data_list

        # ( Run : True ) + ( Scan : False )
        else :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = False
            self.module_result_data["reason"] = "Not Exist External URL in \"form\" Tag."
            self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_form.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlForm(input_url)

    module_instance.scan()
