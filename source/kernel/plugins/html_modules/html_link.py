# [ Kernel ] Module - HTML : html_link.py

from kernel.plugins._base_module import BaseModule

import sys
import tldextract
import re
import time

class HtmlLink(BaseModule) :
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
    def get_url_from_text(self, text) :
        pattern_result = re.search(r"(https?://[^\s\"'>]+)", text.lower())
        
        if pattern_result :

            return pattern_result.group(1)
        
        return ""
    
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

        reason_list = []
        reason_data_list = []
        
        # To Do
        hide_style_list = [
            "display:none",
            "visibility:hidden",
            "opacity:0",
            "width:0",
            "height:0",
            "max-width:0",
            "max-height:0",
            "transform:scale(0)",
        ]

        for a_tag in html_file_bs_object.find_all("a", style = True) :

            a_tag_style = a_tag["style"].replace(" ", "").lower()
            a_tag_text = a_tag.get_text(strip = True)
            a_tag_href = a_tag["href"].strip()

            # [ 1. ] Hide Style
            if any(hide_style in a_tag_style for hide_style in hide_style_list) :

                reason_list.append("Exist Hide Style in \"a\" Tag.")
                reason_data_list.append(a_tag_style)

            # [ 2. ] Different URL
            if a_tag_text and a_tag_href.startswith("http") :

                a_tag_text_url = self.get_url_from_text(a_tag_text)

                different_domain_suffix_flag = self.scan_different_domain_suffix(a_tag_text_url, a_tag_href)

                if different_domain_suffix_flag :

                    reason_list.append("Exist Different URL in \"a\" Tag.")
                    reason_data_list.append(f"\"text\" : {a_tag_text_url} / \"href\" : {a_tag_href}")
            
            # [ 3. ] Open Vulnerability
            if a_tag.get("target") == "_blank" :

                rel_value = a_tag.get("rel", "")
                rel_token_list = rel_value.lower().split()

                if "noopener" not in rel_token_list :

                    reason_list.append("Exist Open Vulnerability in \"a\" Tag.")
                    reason_data_list.append(a_tag)
        
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
            self.module_result_data["reason"] = "Not Exist Hide Style / Different URL / Open Vulnerability in \"a\" Tag."
            self.module_result_data["reason_data"] = None

        self.create_module_result()

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 html_link.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlLink(input_url)

    module_instance.scan()
