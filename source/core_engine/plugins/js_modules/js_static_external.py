# [ Kernel ] Module - JS : js_static_external.py

from core_engine.plugins._base_module import BaseModule

import sys
import tldextract
import re

class JsStaticExternal(BaseModule) :
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
                "pattern_type" : "external_fetch",
                "pattern" : rf"fetch\s*\(\s*['\"]http[s]?://(?!{re.escape(input_domain_suffix)}).*?['\"]",
                "pattern_reason" : "Exist External Fetch in JS."
            },
            {
                "pattern_type" : "external_beacon",
                "pattern" : rf"navigator\.sendBeacon\s*\(\s*['\"]http[s]?://(?!{re.escape(input_domain_suffix)}).*?['\"]",
                "pattern_reason" : "Exist External Beacon in JS."
            },
            {
                "pattern_type" : "external_xmlhttprequest",
                "pattern" : rf"new\s+XMLHttpRequest\s*\(\s*\).*?open\s*\(\s*['\"]POST['\"]?,\s*['\"]http[s]?://(?!{re.escape(input_domain_suffix)}).*?['\"]",
                "pattern_reason" : "Exist External XML HTTP Request in JS."
            },
            {
                "pattern_type": "external_script_src",
                "pattern": rf"script\.src\s*=\s*['\"]http[s]?://(?!{re.escape(input_domain_suffix)}).*?['\"]",
                "pattern_reason": "Exist External Script Source in JS."
            },
            {
                "pattern_type": "external_iframe_src",
                "pattern": rf"(iframe\.src|createElement\s*\(\s*['\"]iframe['\"]\s*\)).*?src\s*=\s*['\"]http[s]?://(?!{re.escape(input_domain_suffix)}).*?['\"]",
                "pattern_reason": "Exist External IFrame Source in JS."
            },
            {
                "pattern_type" : "external_image_request",
                "pattern" : rf"(new\s+Image\(\)|img\.src)\s*=\s*['\"]http[s]?://(?!{re.escape(input_domain_suffix)}).*?['\"]",
                "pattern_reason" : "Exist External Image Request in JS."
            },
        ]

        for pattern_element in pattern_list :

            pattern_result = re.search(pattern_element["pattern"], all_js_code, re.IGNORECASE | re.DOTALL)

            if pattern_result :

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
        self.module_result_data["reason"] = "Not Exist External Pattern in JS."
        self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_static_external.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsStaticExternal(input_url)

    module_instance.scan()
