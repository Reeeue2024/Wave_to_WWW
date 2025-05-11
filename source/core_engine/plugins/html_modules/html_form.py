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
    def scan(self) :
        html_file_bs_object = self.engine_resource.get("html_file_bs_object")

        form_list = html_file_bs_object.find_all("form")

        if not form_list :

            self.module_result_flag = False
            self.module_result_data["ERROR"] = "Fail to Get \"form\" Tag from HTML File."

            self.create_module_result()

            return self.module_result_dictionary   

        external_url_flag = False     

        for form in form_list :

            form_action_data = form.get("action", "")

            external_url_flag = self.is_external_url(self.input_url, form_action_data)

            if external_url_flag :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Exist External URL in \"form\" Tag."
                self.module_result_data["reason_data"] = form_action_data

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Not Exist External URL in \"form\" Tag."
        self.module_result_data["reason_data"] = form_action_data

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
