# [ Kernel ] Module - JS : js_static_hook.py

from core_engine.plugins._base_module import BaseModule

import sys
import re
from concurrent.futures import ThreadPoolExecutor, wait, TimeoutError as FutureTimeoutError

class JsStaticHook(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)
    
    """
    IN : 
    OUT : 
    """
    def run_pattern(self, pattern, code) :
        return re.search(pattern, code, re.IGNORECASE | re.DOTALL)
    
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

        pattern_list = [
            {
                "pattern_type" : "hook_event_keyboard",
                "pattern" : r"addEventListener\s*\(\s*['\"](keydown|keypress|keyup)['\"],\s*function\s*\(.*?\)\s*{.*?}\s*\)",
                "pattern_reason" : "Hook Keyboard Event in JS."
            },
            {
                "pattern_type" : "hook_event_mouse",
                "pattern" : r"addEventListener\s*\(\s*['\"](click|mousedown|mouseup)['\"],\s*function\s*\(.*?\)\s*{.*?}\s*\)",
                "pattern_reason" : "Hook Mouse Event in JS."
            },
            {
                "pattern_type" : "hook_event_submit",
                "pattern" : r"addEventListener\s*\(\s*['\"]submit['\"],\s*function\s*\(.*?\)\s*{.*?}\s*\)",
                "pattern_reason" : "Hook ( Form ) Submit Event in JS."
            },
            {
                "pattern_type" : "hook_event_input",
                "pattern" : r"addEventListener\s*\(\s*['\"](input|change)['\"],\s*function\s*\(.*?\)\s*{.*?}\s*\)",
                "pattern_reason" : "Hook ( Form ) Input / Change Event in JS."
            },
            {
                "pattern_type" : "hook_event_inline_handle",
                "pattern" : r"<[^>]+on(click|keydown|keyup|submit|input)=['\"][^'\"]+['\"]",
                "pattern_reason" : "Hook Inline Event Handle in JS."
            },
            {
                "pattern_type" : "dom_mutate_observe",
                "pattern" : r"new\s+MutationObserver\s*\(\s*function\s*\(.*?\)\s*{.*?}\s*\)",
                "pattern_reason" : "Exist DOM Mutate Observe in JS."
            },
            {
                "pattern_type" : "set_time",
                "pattern" : r"(setInterval|setTimeout)\s*\(\s*function\s*\(.*?\)\s*{.*?}\s*,\s*\d+\s*\)",
                "pattern_reason" : "Exist Set Time in JS."
            },
            {
                "pattern_type" : "event_block",
                "pattern" : r"\.(preventDefault|stopPropagation)\s*\(\s*\)",
                "pattern_reason" : "Exist \"preventDefault()\" in JS."
            },
        ]

        reason_list = []
        reason_data_list = []

        with ThreadPoolExecutor() as executor :

            future_to_reason = {}

            for pattern_element in pattern_list :

                future = executor.submit(self.run_pattern, pattern_element["pattern"], all_js_code)

                future_to_reason[future] = pattern_element
            
            end_work, not_end_work = wait(future_to_reason, timeout = 2)

            for future in end_work :

                pattern_information = future_to_reason[future]
                
                try:
                    result = future.result()

                    if result :

                        reason_list.append(pattern_information["pattern_reason"])
                        reason_data_list.append(result.group(0).strip())
                
                except Exception :
                    continue
        
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
            self.module_result_data["reason"] = "Not Exist Hook Pattern in JS."
            self.module_result_data["reason_data"] = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary


# Module Main
if __name__ == "__main__" :

    if len(sys.argv) != 2 :

        print("How to Use : python3 js_static_hook.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = JsStaticHook(input_url)

    module_instance.scan()
