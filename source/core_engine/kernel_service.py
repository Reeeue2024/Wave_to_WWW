# [ Kernel ] Kernel Service : kernel_service.py

from core_engine.kernel_resource import kernel_resource_instance
from core_engine.engines.full_scan_engine import FullScanEngine
from core_engine.engines.light_scan_engine import LightScanEngine

import requests
import json

class KernelService :
    def __init__(self) :
        # ( Engine ) Result
        self.engine_result_dictionary = {}
        # ( Kernel ) Result
        self.kernel_result_dictionary = {}

    """
    IN : 
    OUT : 
    """
    def run_kernel(self, input_url, engine_type) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service ] Receive Request ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        print(f"  [ + ]  Input URL : {input_url}")
        print(f"  [ + ]  Engine Type : {engine_type}")
        
        # [ 1. ] Get Resource
        # black_list_url = kernel_resource_instance.get_resource("black_list_url")
        # white_list_url = kernel_resource_instance.get_resource("white_list_url")
        
        # print(f"[ DEBUG ] {black_list_url}")
        # print(f"[ DEBUG ] {white_list_url}")

        # [ 2. ] Select Engine
        if engine_type == "full" :
            engine_instance = FullScanEngine(input_url)
        elif engine_type == "light" :
            engine_instance = LightScanEngine(input_url)

        # [ 3. ] Run Engine ( Receive Engine Result )
        self.engine_result_dictionary = engine_instance.run_engine()

        engine_result_flag = False
        engine_result_score = 0
        module_result_dictionary_list = []

        engine_result_flag = self.engine_result_dictionary.get("engine_result_flag")
        engine_result_score = self.engine_result_dictionary.get("engine_result_score") 
        module_result_dictionary_list = self.engine_result_dictionary.get("module_result_dictionary_list")    

        # [ 5. ] Send Response ( Send Kernel Result )
        self.kernel_result_dictionary = {
            "input_url" : input_url,
            "engine_type" : engine_type,
            "engine_result_flag" : engine_result_flag,
            "engine_result_score" : engine_result_score,
            "module_result_dictionary_list" : module_result_dictionary_list,
        }

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service ] Send Response ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        print(f"  [ + ]  Input URL : {self.kernel_result_dictionary.get("input_url")}")
        print(f"  [ + ]  Engine Type : {self.kernel_result_dictionary.get("engine_type")}")
        print(f"  [ + ]  Engine Result Flag : {self.kernel_result_dictionary.get("engine_result_flag")}")
        print(f"  [ + ]  Engine Result Score : {self.kernel_result_dictionary.get("engine_result_score")}")
        print(f"  [ + ]  Module Result Dictionary List : ( ... )")

        print()

        module_result_list = self.kernel_result_dictionary.get("module_result_dictionary_list")
        
        # for index, module_result_element in enumerate(module_result_list, 1) :
        #     print(f"  [ {index:02} ]  Module : {module_result_element['module_class_name']}")
        #     print(f"        ├─ Flag    : {module_result_element['module_result_flag']}")
        #     print(f"        ├─ Score   : {module_result_element['module_score']}")
        #     print(f"        └─ Reason  : {module_result_element['module_result_data']}")
        
        # print()

        return self.kernel_result_dictionary
