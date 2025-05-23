# [ Kernel ] Module - HTML : html_meta_refresh.py

from core_engine.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse, urljoin
import tldextract
import re

class HtmlMetaRefresh(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

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
    def get_redirect_url(self, content) :
        pattern_result = re.search(r"url\s*=\s*[\"']?([^\"';\s]+)", content, re.IGNORECASE)

        if pattern_result :

            return pattern_result.group(1)

        return None

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
        
        meta_refresh_tag_list = html_file_bs_object.find_all("meta", attrs = {"http-equiv" : lambda x : x and x.lower() == "refresh"})

        # Run Fail Case #2
        if not meta_refresh_tag_list :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get \"Meta Refresh\" Tag from HTML File."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary 

        reason_list = []
        reason_data_list = []
        
        for meta_refresh_tag in meta_refresh_tag_list :

            meta_refresh_tag_content = meta_refresh_tag.get("content", "")

            redirect_url = self.get_redirect_url(meta_refresh_tag_content)

            if redirect_url and self.is_external_url(self.input_url, redirect_url) :

                reason_list.append("Exist External URL in Meta Refresh.")
                reason_data_list.append(redirect_url)
        
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
            self.module_result_data["reason"] = "Not Exist External URL in Meta Refresh."
            self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_meta_refresh.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlMetaRefresh(input_url)

    module_instance.scan()
