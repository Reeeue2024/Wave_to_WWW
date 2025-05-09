# [ Core ] Kernel - Kernel Service - Engine : _base_scan_engine.py

import os
import importlib
from concurrent.futures import ThreadPoolExecutor, as_completed

URL_MODULE_DIRECTORY_PATH = "plugins.url_modules"
HTML_MODULE_DIRECTORY_PATH = "plugins.html_modules"
JS_MODULE_DIRECTORY_PATH = "plugins.js_modules"

ENGINE_RESULT_SCORE = 100

class BaseScanEngine :
    def __init__(self, input_url) :
        self.input_url = input_url

        # [ Default ] Module List
        self.module_path_list = [
            (URL_MODULE_DIRECTORY_PATH, "url_homograph"),
            (URL_MODULE_DIRECTORY_PATH, "url_http"),
            (URL_MODULE_DIRECTORY_PATH, "url_tiny_domain"),
            (URL_MODULE_DIRECTORY_PATH, "url_ssl"),
            (URL_MODULE_DIRECTORY_PATH, "url_sub_domain"),
            (URL_MODULE_DIRECTORY_PATH, "url_whois"),

            (HTML_MODULE_DIRECTORY_PATH, "html_form"),
            (HTML_MODULE_DIRECTORY_PATH, "html_iframe"),
            (HTML_MODULE_DIRECTORY_PATH, "html_js_url"),
            (HTML_MODULE_DIRECTORY_PATH, "html_meta_refresh"),
            (HTML_MODULE_DIRECTORY_PATH, "html_resource_url"),

            (JS_MODULE_DIRECTORY_PATH, "js_dom_static"),
            (JS_MODULE_DIRECTORY_PATH, "js_external_static"),
            (JS_MODULE_DIRECTORY_PATH, "js_hook_static"),
            (JS_MODULE_DIRECTORY_PATH, "js_obfuscate_static"),
            (JS_MODULE_DIRECTORY_PATH, "js_redirect_static"),
            (JS_MODULE_DIRECTORY_PATH, "js_script_static"),

            (JS_MODULE_DIRECTORY_PATH, "js_dom_dynamic"),
            (JS_MODULE_DIRECTORY_PATH, "js_external_dynamic"),
            (JS_MODULE_DIRECTORY_PATH, "js_hook_dynamic"),
            (JS_MODULE_DIRECTORY_PATH, "js_obfuscate_dynamic"),
            (JS_MODULE_DIRECTORY_PATH, "js_redirect_dynamic"),
            (JS_MODULE_DIRECTORY_PATH, "js_script_dynamic"),
        ]

        self.module_instance_list = []

        # [ Default ] Module Order List - Synchronous
        self.module_order_list_synchronous = [
            "UrlTinyDomain",
            "UrlHttp",
            "UrlSsl",
        ]

        # [ Default ] Module Order List - Asynchronous
        self.module_order_list_asynchronous = [
            "UrlHomograph",
            "UrlSubDomain",
            "UrlWhois",
            
            "HtmlForm",
            "HtmlIframe",
            "HtmlJsUrl",
            "HtmlMetaRefresh",
            "HtmlResourceUrl",

            "JsDomStatic",
            "JsExternalStatic",
            "JsHookStatic",
            "JsObfuscateStatic",
            "JsRedirectStatic",
            "JsScriptStatic",

            "JsDomDynamic",
            "JsExternalDynamic",
            "JsHookDynamic",
            "JsObfuscateDynamic",
            "JsRedirectDynamic",
            "JsScriptDynamic",
        ]

        self.module_result_dictionary_list = []

        # [ Default ] Module Weight List
        self.module_weight_dictionary = {
            "UrlHomograph" : 10,
            "UrlHttp" : 10,
            "UrlTinyDomain": 10,
            "UrlSsl" : 10,
            "UrlSubDomain" : 10,
            "UrlWhois" : 10,

            "HtmlForm" : 10,
            "HtmlIframe" : 10,
            "HtmlJsUrl" : 10,
            "HtmlMetaRefresh" : 10,
            "HtmlResourceUrl" : 10,

            "JsDomStatic" : 10,
            "JsExternalStatic" : 10,
            "JsHookStatic" : 10,
            "JsObfuscateStatic" : 10,
            "JsRedirectStatic" : 10,
            "JsScriptStatic" : 10,

            "JsDomDynamic" : 10,
            "JsExternalDynamic" : 10,
            "JsHookDynamic" : 10,
            "JsObfuscateDynamic" : 10,
            "JsRedirectDynamic" : 10,
            "JsScriptDynamic" : 10,
        }

        # ( Engine ) Result
        self.engine_result_flag = False
        self.engine_result_score = 0
        self.engine_result_dictionary = {}
    
    """
    IN : 
    OUT : 
    """
    def get_module_class_name(self, module_name) :
        return "".join(word.capitalize() for word in module_name.split("_"))

    """
    IN : 
    OUT : 
    """
    def load_modules(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Load Modules ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        for module_directory_path, module_file_name in self.module_path_list :
            
            import_path = f"{module_directory_path}.{module_file_name}"
            module_file_path = os.path.join(module_directory_path, f"{module_file_name}.py")

            try :
                module_object = importlib.import_module(import_path) # Load Module => Return : < module >

                module_class_name = self.get_module_class_name(module_file_name)
                module_class = getattr(module_object, module_class_name)

                module_instance = module_class(self.input_url) # To Do : input_url => module_context
                module_instance._file_path = module_file_path

                self.module_instance_list.append(module_instance)

                print(f"  [ + ]  {module_class_name:<25} {module_file_path}")
            
            except Exception as e :
                print(f"[ ERROR ] Fail to Load Module : \"{module_file_path}\"")
                print(f"{e}")
        
        print(f"  [ End Log ]  Number of Modules : {len(self.module_instance_list)}")
        
        # print(f"[ DEBUG ] Module Instance List : {self.module_instance_list}")
    
    """
    IN : 
    OUT : 
    """
    def run_a_module(self, module_instance) :
        module_class_name = module_instance.__class__.__name__

        try :
            module_result_dictionary = module_instance.scan()

            self.module_result_dictionary_list.append({
                "module_class_name" : module_class_name,
                "module_run" : True,
                "module_weight" : self.module_weight_dictionary.get(module_class_name),
                "module_result_flag" : module_result_dictionary.get("module_result_flag"),
                "module_result_data" : module_result_dictionary.get("module_result_data"),
            })

            print(f"  [ + ]  {module_class_name:<25} ( Run Module - Success )")

        except Exception as e :
            self.module_result_dictionary_list.append({
                "module_class_name" : module_class_name,
                "module_run" : False,
                "module_error" : {e},
            })

            print(f"  [ ! ]  {module_class_name:<25} ( Run Module - Fail )")
            
    """
    IN : 
    OUT : 
    """
    def run_modules_synchronous(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Run Modules ( Synchronous ) ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        for module_instance in self.module_instance_list :

            module_class_name = module_instance.__class__.__name__

            if module_class_name in self.module_order_list_synchronous :
                
                self.run_a_module(module_instance)

    """
    IN : 
    OUT : 
    """
    def run_modules_asynchronous(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Run Modules ( Asynchronous ) ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        with ThreadPoolExecutor() as executor :

            work_list = []

            for module_instance in self.module_instance_list :

                module_class_name = module_instance.__class__.__name__

                if module_class_name in self.module_order_list_asynchronous :

                    work_list.append(executor.submit(self.run_a_module, module_instance))

            for work in as_completed(work_list) :
                
                work.result()
    
    """
    IN : 
    OUT : 
    """
    def run_modules(self) :
        # print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        # print(" [ Kernel Service - Engine ] Run Modules ...")
        # print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        self.run_modules_synchronous()
        self.run_modules_asynchronous()

        # print(f"[ DEBUG ] Engine Result Dictionary : {self.engine_result_dictionary}")
    
    """
    IN : 
    OUT : 
    """
    def create_engine_result_dictionary(self) :
        # print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        # print(" [ Kernel Service - Engine ] Create Engine Result Dictionary ...")
        # print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        module_result_dictionary_list = []
        
        for module_result_dictionary in self.module_result_dictionary_list :

            module_score = 0

            if module_result_dictionary["module_result_flag"] :

                module_score = module_result_dictionary["module_weight"]

                self.engine_result_score += module_score

            module_result_dictionary_list.append({
                "module_score" : module_score,
                **module_result_dictionary,
            })
        
        if self.engine_result_score >= ENGINE_RESULT_SCORE :

            self.engine_result_flag = True
        
        self.engine_result_dictionary = {
            "engine_result_flag" : self.engine_result_flag,
            "engine_result_score" : self.engine_result_score,
            "module_result_dictionary_list" : module_result_dictionary_list,
        }

    """
    IN : 
    OUT : 
    """
    def run_engine(self) :

        # [ 1. ] Load Modules
        self.load_modules()

        # [ 2. ] Run Modules
        self.run_modules()

        # [ 3. ] Create Engine Result
        self.create_engine_result_dictionary()

        return self.engine_result_dictionary
