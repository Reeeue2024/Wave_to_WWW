# [ Kernel ] Module : _base_module.py

from core_engine.kernel_resource import kernel_resource_instance

import sys

class BaseModule :
    def __init__(self, input_url) :
        self.input_url = input_url
        self.redirect_url = None

        # ( Engine ) Resource
        self.engine_resource = {}

        # ( Module ) Result
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
        self.module_result_dictionary = {
            "module_result_flag" : self.module_result_flag,
            "module_result_data" : self.module_result_data,
        }
    
    """
    IN : 
    OUT : 
    """
    def scan(self) :
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
