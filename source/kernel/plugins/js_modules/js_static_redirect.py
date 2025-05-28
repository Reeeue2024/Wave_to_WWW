# [ Kernel ] Module - JS : js_static_redirect.py

from kernel.plugins._base_module import BaseModule

import sys
import tldextract
import re
from concurrent.futures import ThreadPoolExecutor, wait, TimeoutError as FutureTimeoutError

class JsStaticRedirect(BaseModule) :
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
    def scan_different_domain_suffix(self, one_url, two_url) :
        one_domain_suffix = self.get_domain_suffix(one_url)
        two_domain_suffix = self.get_domain_suffix(two_url)

        return one_domain_suffix != two_domain_suffix

    """
    IN : 
    OUT : 
    """
    def run_pattern(self, pattern, code) :
        return re.search(pattern, code, re.IGNORECASE | re.DOTALL)
    
    """
    IN : 
    OUT : 
    """
    async def scan(self) :
        html_file_script_tag_list = self.engine_resource.get("html_file_script_tag_list", [])
        js_file_dictionary_list = self.engine_resource.get("js_file_dictionary_list", {})

        if not html_file_script_tag_list or not js_file_dictionary_list :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get HTML File / JS File from Engine."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        js_code_list = html_file_script_tag_list[:]
        js_code_list.extend(js_file_dictionary_list.values())

        all_js_code = "\n".join(js_code_list)

        input_domain_suffix = self.get_domain_suffix(self.input_url)

        pattern_list = [
            {
                "pattern_type" : "redirect_location_assign",
                "pattern" : r"(window|document|top|self)?\.?location\.assign\s*\(\s*['\"](?P<url>http[s]?://[^'\"]+)['\"]\s*\)",
                "pattern_reason" : "Exist \"location.assign()\" Redirect in JS."
            },
            {
                "pattern_type" : "redirect_location_replace",
                "pattern" : r"(window|document|top|self)?\.?location\.replace\s*\(\s*['\"](?P<url>http[s]?://[^'\"]+)['\"]\s*\)",
                "pattern_reason" : "Exist \"location.replace()\" Redirect in JS."
            },
            {
                "pattern_type" : "redirect_location_href_assign",
                "pattern" : r"(window|document|top|self)?\.?location\.href\s*=\s*['\"](?P<url>http[s]?://[^'\"]+)['\"]",
                "pattern_reason" : "Exist \"href\" of \"location\" Redirect in JS."
            },
            {
                "pattern_type" : "redirect_location_direct_assign",
                "pattern" : r"(window|document|top|self)?\.?location\s*=\s*['\"](?P<url>http[s]?://[^'\"]+)['\"]",
                "pattern_reason" : "Exist Direct \"location\" Redirect in JS."
            },
            {
                "pattern_type" : "redirect_window_open",
                "pattern" : r"window\.open\s*\(\s*['\"](?P<url>http[s]?://[^'\"]+)['\"]",
                "pattern_reason" : "Exist \"window.open()\" Redirect in JS."
            },
        ]

        reason_list = []
        reason_data_list = []

        with ThreadPoolExecutor() as executor :

            future_to_reason = {}

            for pattern_element in pattern_list :

                future = executor.submit(self.run_pattern, pattern_element["pattern"], all_js_code)

                future_to_reason[future] = pattern_element
            
            end_work, not_end_work = wait(future_to_reason, timeout = 2)

            for future in end_work :

                pattern_information = future_to_reason[future]
                
                try:
                    result = future.result()

                    if result :

                        reason_list.append(pattern_information["pattern_reason"])
                        reason_data_list.append(result.group(0).strip())
                
                except Exception :
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
            self.module_result_data["reason"] = "Not Exist Redirect Pattern in JS."
            self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_static_redirect.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsStaticRedirect(input_url)

    module_instance.scan()
