# [ Core ] Kernel : kernel.py

# ========== # ========== #
"""
Role of "kernel.py"
( 1 ) 다양한 종류의 Module을 Load
( 2 ) Input URL을 바탕으로 각각의 Module을 실행 => ( 각각의 Module은 "scan"을 실행 )
( 3 ) 각각의 Module의 실행 결과를 받는다.
( 4 ) 각각의 Module의 실행 결과를 바탕으로 Score를 설정
( 5 ) Input URL의 Score를 Return
"""
# ========== # ========== #

import importlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class Kernel :
    def __init__(self, input_url) :
        self.input_url = input_url

        # "load_modules" : Load Module 목록
        self.modules_path = "plugins" # [ To Do ] : "plugins" => "modules"
        self.module_instance_list = []

        # "get_result_dictionary" : Load Module의 "Scan" 결과 목록
        self.result_dictionary = {}

        # "get_score_dictionary" : Load Module의 "Scan" 결과를 바탕의 Score 목록
        self.score = 0
        self.score_dictionary = {}
    
    def get_module_class_name(self, module_name) :
        return "".join(word.capitalize() for word in module_name.split("_"))

    """
    IN : 
    OUT : 
    """
    def load_modules(self) :
        module_instance_list = []

        # ( 1 ) Target : Modules Directory 안에 있는 다양한 종류의 Module 파일
        for root, directories, files in os.walk(self.modules_path) :
            for file in files :

                if file.endswith(".py") and not file.startswith("__") :
                    module_full_path = os.path.join(root, file) # Full Path ( 예 ) : "modules/url_modules/url_homograph.py"
                    module_import_path = module_full_path[:-3].replace(os.sep, ".") # Import Path ( 예 ) : "modules.url_modules.url_homograph"

                    module_name = (os.path.basename(module_full_path))[:-3] # Module Name ( 예 ) : "url_homograph"
                    module_class_name = self.get_module_class_name(module_name) # Class Name ( 예 ) : "UrlHomograph"

                    try :
                        # ( 2 ) Module을 Dynamic Load
                        module = importlib.import_module(module_import_path)

                        module_string = f"{module_class_name}"
                        print(f"  [ + ]  {module_string:<25} {module_full_path}")

                        module_class = getattr(module, module_class_name)
                        module_instance = module_class(self.input_url)

                        # ( 3 ) Original 파일 Path를 Module Instance에 저장
                        module_instance._file_path = module_full_path

                        module_instance_list.append(module_instance)

                    except Exception as e :
                        print(f"[ ERROR ] Fail to Load Module \"{module_full_path}\" : {e}")
        
        # print(f"[ DEBUG ] Module Instance List : {module_instance_list}")

        self.module_instance_list = module_instance_list
            
    """
    IN : 
    OUT : 
    """
    def get_result_dictionary(self) :
        result_dictionary = {}

        # ( 1 ) 각각의 Thread 실행
        with ThreadPoolExecutor() as executor :
            work_list = [executor.submit(self.run_module_scan, m) for m in self.module_instance_list]
            
            for work_result in as_completed(work_list) :
                key, result = work_result.result()
                result_dictionary[key] = result

        # print(f"[ DEBUG ] Result Dictionary : {result_dictionary}")

        self.result_dictionary = result_dictionary
    
    """
    IN : 
    OUT : 
    """
    def run_module_scan(self, module_instance) :
        try :
            result = module_instance.scan()

            class_name = module_instance.__class__.__name__
            module_file_path = getattr(module_instance, "_file_path", "Fail to Get File Path")
            key = f"{class_name} ( Module : {module_file_path} )"

            return (key, result)
        
        except Exception as e :
            class_name = module_instance.__class__.__name__
            module_file_path = getattr(module_instance, "_file_path", "Fail to Get File Path")
            key = f"{class_name} ( Module : {module_file_path} )"

            return (key, f"ERROR : {e}")
            
    """
    IN : 
    OUT : 
    """
    def get_score_dictionary(self) :
        # [ To Do ]
        module_weight_list = {
            "url_homograph" : 10,
            "url_http" : 10,
            "url_shorting": 10,
            "url_ssl" : 10,
            "url_sub_domain" : 10,
            "url_whois" : 10,
            "html_form" : 10,
            "html_iframe" : 10,
            "html_js" : 10,
            "html_meta" : 10,
            "html_url" : 10,
            "js_dom_dynamic" : 10,
            "js_dom_static" : 10,
            "js_exfil_dynamic" : 10,
            "js_exfil_static" : 10,
            "js_hooking_dynamic" : 10,
            "js_hooking_static" : 10,
            "js_obfuscation_dynamic" : 10,
            "js_obfuscation_static" : 10,
            "js_redirect_dynamic" : 10,
            "js_redirect_static" : 10,
            "js_script_dynamic" : 10,
            "js_script_static" : 10,
        }

        score = 0
        score_dictionary = {}

        # ( 1 ) Target : 각각의 Module Instance
        for module_instance in self.module_instance_list :
            class_name = module_instance.__class__.__name__
            module_file_path = getattr(module_instance, "_file_path", "Fail to Get File Path")
            result_dictionary_key = f"{class_name} ( Module : {module_file_path} )"
            result = self.result_dictionary.get(result_dictionary_key, False) # Module Instance의 결과를 Get

            for keyword, weight in module_weight_list.items() :
                # print(f"[ DEBUG ] {keyword} ( {weight} ) : {result}")

                # ( 2 ) "module_weight_list" 안에 해당 Module Instance가 있을 경우 + 해당 Module Instance의 결과 True 경우 => Score +
                if ( keyword in result_dictionary_key ) and ( result is True ) :
                    score += weight
                    score_dictionary[class_name] = weight # 그리고 "score_dictionary"에 추가

        # print(f"[ DEBUG ] Score : {score}")
        # print(f"[ DEBUG ] Score Dictionary : {score_dictionary}")
        
        self.score = score
        self.score_dictionary = score_dictionary

    """
    IN : 
    OUT : 
    """
    def start(self) :
        print()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel ] Load Modules ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        self.load_modules()

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f" [ Kernel ] Total Modules : {len(self.module_instance_list)}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print()

        self.get_result_dictionary()

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel ] Calculate Score ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        self.get_score_dictionary()

        for class_name, score in self.score_dictionary.items() :
            print(f"  [ + ]  {class_name:<25} {score}")

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f" [ Kernel ] Total Score : {self.score}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # [ To Do ]
        if self.score >= 100 :
            return True
        else :
            return False
