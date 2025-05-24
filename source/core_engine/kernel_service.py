# [ Kernel ] Kernel Service : kernel_service.py

from core_engine.kernel_resource import kernel_resource_instance
from core_engine.engines.full_scan_engine import FullScanEngine
from core_engine.engines.light_scan_engine import LightScanEngine

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

        try :
            if not input_url or not isinstance(input_url, str) :
                raise ValueError("[ ERROR ] \"Input URL\" is INVALID.")

            if not engine_type or engine_type not in ("full", "light") :
                raise ValueError("[ ERROR ] \"Engine Type\" is INVALID.")

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
            if engine_type == "light" :
                engine_instance = LightScanEngine(input_url)

            # [ 3. ] Run Engine ( Receive Engine Result )
            self.engine_result_dictionary = engine_instance.run_engine()

            engine_result_flag = self.engine_result_dictionary.get("engine_result_flag")
            engine_result_score = self.engine_result_dictionary.get("engine_result_score")
            engine_result_run_true_score = self.engine_result_dictionary.get("engine_result_run_true_score")
            engine_result_run_true_weight = self.engine_result_dictionary.get("engine_result_run_true_weight")
            module_result_dictionary_list = self.engine_result_dictionary.get("module_result_dictionary_list")    

            # [ 5. ] Send Response ( Send Kernel Result )
            self.kernel_result_dictionary = {
                "input_url" : input_url,
                "engine_type" : engine_type,
                "engine_result_flag" : engine_result_flag,
                "engine_result_score" : engine_result_score,
                "engine_result_run_true_score" : engine_result_run_true_score,
                "engine_result_run_true_weight" : engine_result_run_true_weight,
                "module_result_dictionary_list" : module_result_dictionary_list,
                "error_flag" : False,
                "error_type" : None,
            }

        except Exception as e :
            print(f"[ ERROR ] Fail to Run - Kernel Service : {type(e).__name__}")
            print(f"{e}")

            self.kernel_result_dictionary = {
                "input_url" : input_url,
                "engine_type" : engine_type,
                "engine_result_flag" : False,
                "engine_result_score" : 0,
                "engine_result_run_true_score" : 0,
                "engine_result_run_true_weight" : 0,
                "module_result_dictionary_list" : None,
                "error_flag" : True,
                "error_type" : type(e).__name__,
            }

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service ] Send Response ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        print(f"  [ + ]  Input URL : {self.kernel_result_dictionary.get('input_url')}")
        print(f"  [ + ]  Engine Type : {self.kernel_result_dictionary.get('engine_type')}")
        print(f"  [ + ]  Engine Result Flag : {self.kernel_result_dictionary.get('engine_result_flag')}")
        print(f"  [ + ]  Engine Result Score : {self.kernel_result_dictionary.get('engine_result_score')}")
        print(f"  [ + ]  Engine Result Run True Score : {self.kernel_result_dictionary.get('engine_result_run_true_score')}")
        print(f"  [ + ]  Engine Result Run True Weight : {self.kernel_result_dictionary.get('engine_result_run_true_weight')}")
        print(f"  [ + ]  Module Result Dictionary List : ( ... )")
        print(f"  [ + ]  ERROR Flag : {self.kernel_result_dictionary.get('error_flag')}")
        print(f"  [ + ]  ERROR Type : {self.kernel_result_dictionary.get('error_type')}")

        print()

        return self.kernel_result_dictionary
