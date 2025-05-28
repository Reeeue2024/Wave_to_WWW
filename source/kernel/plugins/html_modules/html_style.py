# [ Kernel ] Module - HTML : html_style.py

from kernel.plugins._base_module import BaseModule

import sys
from urllib.parse import urlparse
import tinycss2

class HtmlStyle(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

    """
    IN : 
    OUT : 
    """
    def get_z_index(self, style_data) :
        try :
            for style_element in style_data.split(";") :

                if "z-index" in style_element :

                    key, value = style_element.split(":")

                    if "z-index" in key.strip().lower() :

                        return int(value.strip())
        
        except :
            pass

        try :
            declaration_list = tinycss2.parse_declaration_list(style_data)

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
        
        password_tag = html_file_bs_object.find("input", {"type" : "password"})

        # Run Fail Case #2
        if not password_tag :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get \"Password Tag\" from HTML File."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

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
        overlay_position_list = [
            "position:absolute",
            "position:fixed",
        ]
        
        # To Do
        overlay_size_list = [
            "width:100%",
            "height:100%",
            "width:9999px",
            "height:9999px",
            "top:0",
            "left:0",
            "bottom:0",
            "right:0",
            "inset:0",
        ]

        for style_element in html_file_bs_object.find_all(style = True) :

            style = style_element.get("style", "").replace(" ", "").lower()
            
            # [ 1. ] Z Index
            z_index = self.get_z_index(style_element)

            if z_index is not None and z_index >= 100 :

                reason_list.append("Exist High Z Index with Password Tag.")
                reason_data_list.append(style_element)

            # [ 2. ] Hide Style
            if any(hide_style in style for hide_style in hide_style_list) :

                reason_list.append("Exist Hide Style with Password Tag.")
                reason_data_list.append(style)

            # [ 3. ] Overlay Style
            overlay_position_flag = any(overlay_position in style for overlay_position in overlay_position_list)
            overlay_size_flag = any(overlay_size in style for overlay_size in overlay_size_list)

            if overlay_position_flag and overlay_size_flag :

                reason_list.append("Exist Overlay Style with Password Tag.")
                reason_data_list.append(style)

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
            self.module_result_data["reason"] = "Not Exist Z Index / Hide Style / Overlay Style with Password Tag."
            self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_style.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlStyle(input_url)

    module_instance.scan()
