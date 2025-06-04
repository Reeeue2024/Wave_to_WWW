# [ Kernel ] Module - HTML : html_resource_url.py

from kernel.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import tldextract
import time

class HtmlResourceUrl(BaseModule) :
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
    async def scan(self) :
        start_time = time.time()

        html_file_bs_object = self.engine_resource.get("html_file_bs_object")

        # Run Fail Case #1
        if not html_file_bs_object :

            self.module_run = False
            self.module_run_time = round(time.time() - start_time, 2)
            self.module_error = "[ ERROR ] Fail to Get HTML File from Engine."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        resource_url_list = []

        # [ 1. ] Link
        for tag in html_file_bs_object.find_all("link", href = True) :

            resource_url_list.append(tag["href"])

        # [ 2. ] Script
        for tag in html_file_bs_object.find_all("script", src = True) :

            resource_url_list.append(tag["src"])

        # [ 3. ] Image
        for tag in html_file_bs_object.find_all("img", src = True) :

            resource_url_list.append(tag["src"])

        # [ 4. ] Input Image
        for tag in html_file_bs_object.find_all("input", attrs={"type" : "image"}) :

            if tag.get("src") :

                resource_url_list.append(tag["src"])
        
        # [ 5. ] audio / video / source / track
        for tag in html_file_bs_object.find_all(["audio", "video", "source", "track"], src = True) :

            resource_url_list.append(tag["src"])

        # [ 6. ] To Do

        # Run Fail Case #2
        if not resource_url_list :

            self.module_run = False
            self.module_run_time = round(time.time() - start_time, 2)
            self.module_error = "[ ERROR ] Fail to Get \"URL\" in Resource from HTML File."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary
        
        reason_list = []
        reason_data_list = []

        for resource_url in resource_url_list :

            if self.is_external_url(self.input_url, resource_url) :

                reason_list.append("Exist External URL in Resource.")
                reason_data_list.append(resource_url)

        # ( Run : True ) + ( Scan : True )
        if reason_list or reason_data_list :

            self.module_run = True
            self.module_run_time = round(time.time() - start_time, 2)
            self.module_error = None
            self.module_result_flag = True
            self.module_result_data["reason"] = reason_list
            self.module_result_data["reason_data"] = reason_data_list

        # ( Run : True ) + ( Scan : False )
        else :

            self.module_run = True
            self.module_run_time = round(time.time() - start_time, 2)
            self.module_error = None
            self.module_result_flag = False
            self.module_result_data["reason"] = "Not Exist External URL in Resource."
            self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary
    
# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_resource_url.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlResourceUrl(input_url)

    module_instance.scan()
