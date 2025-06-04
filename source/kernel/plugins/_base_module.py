# [ Kernel ] Module : _base_module.py

from kernel.kernel_resource import kernel_resource_instance

import sys

class BaseModule :
    def __init__(self, input_url) :
        self.input_url = input_url
        self.redirect_url = None

        self.module_time_out = 10

        # ( Engine ) Resource
        self.engine_resource = {}

        # ( Module ) Result
        self.module_run = False
        self.module_run_time = 0
        self.module_error = None
        self.module_result_flag = False
        self.module_result_data = {}

        self.module_result_dictionary = {}
    
    """
    IN : 
    OUT : 
    """
    def get_kernel_resource(self, key) :
        return kernel_resource_instance.get_resource(key)

    """
    IN : 
    OUT : 
    """
    def get_engine_resource(self, engine_resource) :
        self.engine_resource = engine_resource

    """
    IN : 
    OUT : 
    """
    def create_module_result(self) :
        if isinstance(self.module_result_data, dict) :

            for key in ["reason", "reason_data"] :

                value = self.module_result_data.get(key)

                if isinstance(value, list) :

                    new_list = []

                    all_element_count = len(value)
                    max_element_count = 10
                    max_element_length = 100

                    for item in value[:max_element_count] :

                        if isinstance(item, str) and len(item) > max_element_length :

                            new_list.append(item[:max_element_length] + " ( ... )")

                        else :

                            new_list.append(item)
                    
                    if all_element_count > max_element_count :

                        new_list.append(f"[ More ] {all_element_count - max_element_count} \"Reason + Reason Data\" Exist.")

                    self.module_result_data[key] = new_list

        self.module_result_dictionary = {
            "module_run" : self.module_run,
            "module_run_time" : self.module_run_time,
            "module_error" : self.module_error,
            "module_result_flag" : self.module_result_flag,
            "module_result_data" : self.module_result_data,
        }
    
    """
    IN : 
    OUT : 
    """
    async def scan(self) :
        print()
    
        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 _base_module.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = BaseModule(input_url)
    
    module_instance.scan()
