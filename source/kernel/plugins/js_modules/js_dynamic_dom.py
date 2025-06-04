# [ Kernel ] Module - JS : js_dynamic_dom.py

from kernel.plugins._base_module import BaseModule

import sys
import json
import os
import asyncio
import time

class JsDynamicDom(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

    """
    IN : 
    OUT : 
    """
    async def scan(self) :
        start_time = time.time()

        js_directory_path = os.path.dirname(os.path.abspath(__file__))
        js_file_path = os.path.abspath(os.path.join(js_directory_path, "js_dynamic_dom.js"))

        try :
            # [ 1. ] Create Asynchronous Process - "Node JS"
            process = await asyncio.create_subprocess_exec(
                "node", js_file_path, self.input_url,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            # [ 2. ] Get "Time-Out" From Engine
            time_out = getattr(self, "time_out_module", 20)

            # [ 3. ] Set "Time-Out"
            try :
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout = time_out)

            except asyncio.TimeoutError :
                process.kill()

                await process.communicate()

                self.module_run = False
                self.module_run_time = round(time.time() - start_time, 2) # Add Execute Time in JS
                self.module_error = f"[ ERROR ] TIME OUT : {time_out}"
                self.module_result_flag = False
                self.module_result_data = None

                self.create_module_result()

                return self.module_result_dictionary

            result_js = stdout.decode().strip()

        except Exception as e :
            self.module_run = False
            self.module_run_time = round(time.time() - start_time, 2) # Add Execute Time in JS
            self.module_error = f"[ ERROR ] {e}"
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        try :
            result_object = json.loads(result_js)

            # print(f"[ DEBUG ] JSON : {result_object}")

            self.module_run = not bool(result_object.get("error_log_list")) # Empty : ( Run ) True / Not Empty : ( Run ) False
            self.module_result_flag = bool(result_object.get("flag"))

            # print(f"[ DEBUG ] Type of Flag : {type(self.module_result_flag)}")
            # print(f"[ DEBUG ] Value of Flag : {self.module_result_flag}")

            if self.module_run :

                self.module_error = None

                # ( Run : True ) + ( Result : True )
                if self.module_result_flag :

                    self.module_result_data["reason"] = result_object.get("reason_log_list")
                    self.module_result_data["reason_data"] = result_object.get("reason_data_log_list")
                
                # ( Run : True ) + ( Result : False )
                else :

                    self.module_result_data["reason"] = "Not Exist DOM Action."
                    self.module_result_data["reason_data"] = None

            # ( Run : False )
            else :

                error_log_list = result_object.get("error_log_list", [])

                self.module_error = error_log_list
                self.module_result_flag = False
                self.module_result_data = None
        
        except json.JSONDecodeError as e :
            print(f"[ DEBUG ] JSON : {result_js}")

            self.module_run = False
            self.module_run_time = round(time.time() - start_time, 2) # Add Execute Time in JS
            self.module_error = f"[ ERROR ] {e}"
            self.module_result_flag = False
            self.module_result_data = None

        except Exception as e :
            print(f"[ DEBUG ] JSON : {result_js}")
            
            self.module_run = False
            self.module_run_time = round(time.time() - start_time, 2) # Add Execute Time in JS
            self.module_error = f"[ ERROR ] {e}"
            self.module_result_flag = False
            self.module_result_data = None

        self.module_run_time = round(time.time() - start_time, 2) # Add Execute Time in JS

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_dynamic_dom.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsDynamicDom(input_url)

    module_instance.scan()
