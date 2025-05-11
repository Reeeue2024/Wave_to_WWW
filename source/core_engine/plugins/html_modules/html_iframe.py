# [ Kernel ] Module - HTML : html_iframe.py

from core_engine.plugins._base_module import BaseModule

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
    def scan(self) :
        html_file_bs_object = self.engine_resource.get("html_file_bs_object")

        iframe_tag_list = html_file_bs_object.find_all("iframe", src = True)
        object_tag_list = html_file_bs_object.find_all("object", data = True)
        embed_tag_list = html_file_bs_object.find_all("embed", src = True)

        all_tag_list = iframe_tag_list + object_tag_list + embed_tag_list

        if not all_tag_list :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Not Exist \"iframe / object / embed\" Tag in HTML File."
            self.module_result_data["reason_data"] = ""

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        for tag in all_tag_list :

            if tag.name in ["iframe", "embed"] :

                attribute = "src"

            else :
                attribute = "data"
                        
            # [ 1. ] External URL
            tag_url = tag.get(attribute, "")

            if self.is_external_url(self.input_url, tag_url) :
                
                self.module_result_flag = True
                self.module_result_data["reason"] = f"Exist External URL in \"{tag.name}\" Tag."
                self.module_result_data["reason_data"] = tag_url

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary
            
            tag_style = tag.get("style", "").lower()

            # [ 2-1. ] Hide Style
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

            if any(hide_style in tag_style for hide_style in hide_style_list) :

                self.module_result_flag = True
                self.module_result_data["reason"] = f"Exist Hide Style in \"{tag.name}\" Tag."
                self.module_result_data["reason_data"] = tag_style

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

            # [ 2-2. ] Overlay Style
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

            if any(tag.get(attribute) == value for attribute, value in overlay_style_list) :
            
                self.module_result_flag = True
                self.module_result_data["reason"] = "Exist Overlay Style in \"{tag.name}\" Tag.."
                self.module_result_data["reason_data"] = tag_style

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Not Exist Hide Style / Overlay Style in \"iframe / object / embed\" Tag."
        self.module_result_data["reason_data"] = ""

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
