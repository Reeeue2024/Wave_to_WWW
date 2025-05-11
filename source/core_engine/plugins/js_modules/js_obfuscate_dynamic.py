# [ Kernel ] Module - JS : js_obfuscate_dynamic.py

from core_engine.plugins._base_module import BaseModule

import sys
import subprocess
import json
import os

class JsObfuscateDynamic(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        js_directory_path = os.path.dirname(os.path.abspath(__file__))
        js_file_path = os.path.abspath(os.path.join(js_directory_path, "js_obfuscate_dynamic.js"))

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

            self.module_result_data["log_list"] = result_object.get("log_list", [])
            self.module_result_data["score"] = result_object.get("score", 0)

            if result_object.get("score", 0) >= 50 :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Obfuscate Dynamic Score : High."
            
            elif result_object.get("score", 0) >= 20 :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Obfuscate Dynamic Score : Not High / Not Low."
            
            else :

                self.module_result_flag = False
                self.module_result_data["reason"] = "Obfuscate Dynamic Score : Low."

        except json.JSONDecodeError :
            self.module_result_flag = True
            self.module_result_data["reason"] = "Fail to Parse Result of JS."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_obfuscate_dynamic.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsObfuscateDynamic(input_url)

    module_instance.scan()