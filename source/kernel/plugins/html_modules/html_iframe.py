# [ Kernel ] Module - HTML : html_iframe.py

from kernel.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import tldextract

class HtmlIframe(BaseModule) :
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
        html_file_bs_object = self.engine_resource.get("html_file_bs_object")

        # Run Fail Case #1
        if not html_file_bs_object :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get HTML File from Engine."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        iframe_tag_list = html_file_bs_object.find_all("iframe", src = True)
        object_tag_list = html_file_bs_object.find_all("object", data = True)
        embed_tag_list = html_file_bs_object.find_all("embed", src = True)

        all_tag_list = iframe_tag_list + object_tag_list + embed_tag_list

        # Run Fail Case #2
        if not all_tag_list :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get \"iframe / object / embed\" Tag from HTML File."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        reason_list = []
        reason_data_list = []

        # To Do
        hide_style_list = [
            "display:none",
            "opacity:0",
            "visibility:hidden",
            "height:0",
            "width:0",
            "max-height:0",
            "max-width:0",
            "transform:scale(0)",
            "overflow:hidden",
        ]

        # To Do
        overlay_style_list = [
            ("width", "100%"),
            ("height", "100%"),
            ("max-width", "100%"),
            ("max-height", "100%"),
            ("top", "0"),
            ("left", "0"),
            ("bottom", "0"),
            ("right", "0"),
            ("inset", "0"),
            ("position", "absolute"),
            ("position", "fixed"),
        ]

        for tag in all_tag_list :

            if tag.name in ["iframe", "embed"] :

                attribute = "src"

            else :
                attribute = "data"
                        
            # [ 1. ] External URL
            tag_url = tag.get(attribute, "")

            if self.is_external_url(self.input_url, tag_url) :

                reason_list.append(f"Exist External URL in \"{tag.name}\" Tag.")
                reason_data_list.append(tag_url)
            
            tag_style = tag.get("style", "").lower()

            # [ 2-1. ] Hide Style
            if any(hide_style in tag_style for hide_style in hide_style_list) :

                reason_list.append(f"Exist Hide Style in \"{tag.name}\" Tag.")
                reason_data_list.append(tag_style)

            # [ 2-2. ] Overlay Style
            if any(tag.get(attribute) == value for attribute, value in overlay_style_list) :

                reason_list.append(f"Exist Overlay Style in \"{tag.name}\" Tag.")
                reason_data_list.append(tag_style)
        
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
            self.module_result_data["reason"] = "Not Exist Hide Style / Overlay Style in \"iframe / object / embed\" Tag."
            self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_iframe.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlIframe(input_url)

    module_instance.scan()
