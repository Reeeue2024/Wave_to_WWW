# [ Kernel ] Module - JS : js_static_redirect.py

from core_engine.plugins._base_module import BaseModule

import sys
import tldextract
import re

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

        for pattern_element in pattern_list :

            pattern_result = re.search(pattern_element["pattern"], all_js_code, re.IGNORECASE | re.DOTALL)

            if pattern_result :

                redirect_url = pattern_result.group("url").strip()
                redirect_domain_suffix = self.get_domain_suffix(redirect_url)

                different_domain_suffix_flag = self.scan_different_domain_suffix(input_domain_suffix, redirect_domain_suffix)

                if different_domain_suffix_flag :

                    reason_data = pattern_result.group(0).strip()

                    self.module_run = True
                    self.module_error = None
                    self.module_result_flag = True
                    self.module_result_data["reason"] = pattern_element["pattern_reason"]
                    self.module_result_data["reason_data"] = reason_data

                    self.create_module_result()

                    # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                    return self.module_result_dictionary

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
