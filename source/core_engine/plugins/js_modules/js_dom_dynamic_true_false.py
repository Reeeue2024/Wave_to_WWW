# [ Core ] Module - JS : js_dom_dynamic.py ( True / False )

from plugins._base_module import BaseModule

import sys
import subprocess
import json
import os

class JsDomDynamic(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        js_directory_path = os.path.dirname(os.path.abspath(__file__))
        js_file_path = os.path.abspath(os.path.join(js_directory_path, "js_dom_dynamic.js"))

        try :
            result_js = subprocess.check_output(
                ["node", js_file_path, self.input_url],
                universal_newlines = True,
                timeout = 10
            )
        
        except Exception as e :
            self.module_result_flag = False
            self.module_result_data["reason"] = f"Fail to Execute JS : {e}"

            self.create_module_result()

            return self.module_result_dictionary

        try :
            result_object = json.loads(result_js)

            log_list = result_object.get("log_list", [])
            flag = result_object.get("flag", False)

            if flag :

                self.module_result_flag = True
                self.module_result_data["reason"] = "DOM Dynamic Exist."
                self.module_result_data["log_list"] = log_list
            
            else :
                self.module_result_flag = False
                self.module_result_data["reason"] = "DOM Dynamic Not Exist."

        except json.JSONDecodeError :
            self.module_result_flag = True
            self.module_result_data["reason"] = "Fail to Parse Result of JS."

        self.create_module_result()

        print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_dom_dynamic.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsDomDynamic(input_url)

    module_instance.scan()
