# [ Core ] Module - HTML : html_iframe.py

# Tag - Iframe / Object / Embed + Style ( Hidden / Absolute / Z-Index )

from plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
import tinycss2 # pip install tinycss2

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
    def is_external_domain(self, base_url, input_url) :
        base_domain = self.get_domain_suffix(base_url)

        input_domain = self.get_domain_suffix(input_url)

        return base_domain != input_domain

    """
    IN : 
    OUT : 
    """
    def get_z_index(self, style_string) :
        try :
            for rule in style_string.split(";") :

                if "z-index" in rule :

                    key, value = rule.split(":")

                    if "z-index" in key.strip().lower() :

                        return int(value.strip())
        
        except :
            pass

        try :
            declaration_list = tinycss2.parse_declaration_list(style_string)

            for declaration in declaration_list :

                if declaration.type == "declaration" and declaration.name == "z-index" and not declaration.invalid :

                    for token in declaration.value :
                        
                        if token.type == "number" :
                            
                            return int(token.value)
        except :
            pass

        return None

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        headers = {
            "User-Agent" : "Mozilla/5.0"
        }

        try :
            response = requests.get(self.input_url, headers = headers, timeout = 5)

            response.raise_for_status()

            html = response.text

        except requests.RequestException as e :

            self.module_result_flag = False
            self.module_result_data["reason"] = f"Fail to Get HTML."

            self.create_module_result()

            return self.module_result_dictionary

        bs = BeautifulSoup(html, "html.parser")

        base_url = self.input_url

        iframe_tag_list = bs.find_all("iframe", src = True)
        object_tag_list = bs.find_all("object", data = True)
        embed_tag_list = bs.find_all("embed", src = True)

        all_tag_list = iframe_tag_list + object_tag_list + embed_tag_list

        if not all_tag_list :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Tag ( Iframe / Object / Embed ) Not Exist."

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        for tag in all_tag_list :

            # [ 1-1. ]
            attribute = "src" if tag.name in ["iframe", "embed"] else "data"
            
            tag_url = tag.get(attribute, "")

            if self.is_external_domain(base_url, tag_url) :
                
                self.module_result_flag = True
                self.module_result_data["reason"] = "External Resource is in Tag."
                self.module_result_data["tag_name"] = tag.name
                self.module_result_data["tag_url"] = tag_url

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

            # [ 1-2. ]
            tag_style = tag.get("style", "").lower()

            if any(keyword in tag_style for keyword in ["display:none", "opacity:0", "visibility:hidden"]) :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Hide Style in Tag."
                self.module_result_data["tag_name"] = tag.name
                self.module_result_data["tag_style"] = tag_style

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

            # [ 1-3. ]
            if tag.get("width") == "100%" or tag.get("height") == "100%" :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Full Screen Overlay."
                self.module_result_data["tag_name"] = tag.name
                self.module_result_data["tag_data"] = tag

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        password_tag = bs.find("input", {"type" : "password"})

        if password_tag :

            # [ 2-1.]
            for tag in bs.find_all(style = True) :
                
                tag_style = tag["style"]
                
                z_index = self.get_z_index(tag_style)

                if z_index is not None and z_index >= 100 :

                    self.module_result_flag = True
                    self.module_result_data["reason"] = "Password Tag + High Z-Index."
                    self.module_result_data["z_index"] = z_index

                    self.create_module_result()

                    # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                    return self.module_result_dictionary

            # [ 2-2. ]
            for tag in bs.find_all("div", style = True) :

                if "position:absolute" in tag["style"].lower() :

                    self.module_result_flag = True
                    self.module_result_data["reason"] = "Password Tag + Absolute Position Overlay."
                    self.module_result_data["tag"] = "div"

                    self.create_module_result()

                    # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                    return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Not in Tag."

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
