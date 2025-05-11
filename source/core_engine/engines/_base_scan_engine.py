# [ Kernel ] Kernel Service - Engine : _base_scan_engine.py

import os
import importlib
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

URL_MODULE_DIRECTORY_PATH = "core_engine.plugins.url_modules"
HTML_MODULE_DIRECTORY_PATH = "core_engine.plugins.html_modules"
JS_MODULE_DIRECTORY_PATH = "core_engine.plugins.js_modules"

# [ Default ]
ENGINE_RESULT_SCORE = 100

class BaseScanEngine :
    def __init__(self, input_url) :
        self.input_url = input_url
        self.redirect_url = None

        self.engine_resource = {}

        # [ Default ] Module List
        self.module_path_list = [
            (URL_MODULE_DIRECTORY_PATH, "url_short"),
            
            (URL_MODULE_DIRECTORY_PATH, "url_homograph"),
            (URL_MODULE_DIRECTORY_PATH, "url_http"),
            (URL_MODULE_DIRECTORY_PATH, "url_ssl"),
            (URL_MODULE_DIRECTORY_PATH, "url_sub_domain"),
            (URL_MODULE_DIRECTORY_PATH, "url_whois"),

            (HTML_MODULE_DIRECTORY_PATH, "html_form"),
            (HTML_MODULE_DIRECTORY_PATH, "html_iframe"),
            (HTML_MODULE_DIRECTORY_PATH, "html_js_url"),
            (HTML_MODULE_DIRECTORY_PATH, "html_meta_refresh"),
            (HTML_MODULE_DIRECTORY_PATH, "html_resource_url"),
            (HTML_MODULE_DIRECTORY_PATH, "html_style"),

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
            "UrlShort",
        ]

        # [ Default ] Module Order List - Asynchronous
        self.module_order_list_asynchronous = [
            "UrlHttp",
            "UrlSsl",
            "UrlHomograph",
            "UrlSubDomain",
            "UrlWhois",
            
            "HtmlForm",
            "HtmlIframe",
            "HtmlJsUrl",
            "HtmlMetaRefresh",
            "HtmlResourceUrl",
            "HtmlStyle",

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
            "UrlShort": 10,

            "UrlHomograph" : 10,
            "UrlHttp" : 10,
            "UrlSsl" : 10,
            "UrlSubDomain" : 10,
            "UrlWhois" : 10,

            "HtmlForm" : 10,
            "HtmlIframe" : 10,
            "HtmlJsUrl" : 10,
            "HtmlMetaRefresh" : 10,
            "HtmlResourceUrl" : 10,
            "HtmlStyle" : 10,

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
    def set_engine_resource(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Set Engine Resource ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        try :
            headers = {
                "User-Agent" : (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
            }

            response = requests.get(self.input_url, headers = headers, timeout = 5)

            response.raise_for_status()

            bs = BeautifulSoup(response.text, "html.parser")

            html_file_script_tag_list = []
            js_file_dictionary = {}

            for script_tag in bs.find_all("script") :

                if script_tag.get("src") :

                    js_file_url = urljoin(self.input_url, script_tag["src"])

                    try :
                        js_file = requests.get(js_file_url, timeout = 5).text

                        js_file_dictionary[js_file_url] = js_file
                    except :
                        continue
                else :

                    if script_tag.string :

                        html_file_script_tag_list.append(script_tag.string.strip())
                
            self.engine_resource["html_file_bs_object"] = bs
            self.engine_resource["html_file_script_tag_list"] = html_file_script_tag_list
            self.engine_resource["js_file_dictionary_list"] = js_file_dictionary

        except Exception as e :
            print(f"[ ERROR ] Fail to Set Engine Reousrce : {self.input_url}")
            print(f"{e}")
    
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
    def load_module(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Load Module ...")
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

                module_instance.get_engine_resource(self.engine_resource) # Get Engine Resource

                self.module_instance_list.append(module_instance)

                print(f"  [ + ]  {module_class_name:<25} {module_file_path}")
            
            except Exception as e :
                print(f"[ ERROR ] Fail to Load Module : \"{module_file_path}\"")
                print(f"{e}")
        
        print(f"  [ End Log ]  Number of Module : {len(self.module_instance_list)}")
        
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

            print(f"{e}")
            
    """
    IN : 
    OUT : 
    """
    def run_module_synchronous(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Run Module ( Synchronous ) ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        for module_instance in self.module_instance_list :

            module_class_name = module_instance.__class__.__name__

            if module_class_name in self.module_order_list_synchronous :
                
                self.run_a_module(module_instance)

                if module_class_name == "UrlShort" :

                    redirect_url = self.engine_resource.get("redirect_url")

                    if redirect_url and self.input_url != redirect_url :

                        self.input_url = redirect_url

    """
    IN : 
    OUT : 
    """
    def run_module_asynchronous(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Run Module ( Asynchronous ) ...")
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
    def run_module(self) :
        # print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        # print(" [ Kernel Service - Engine ] Run Module ...")
        # print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        self.run_module_synchronous()
        self.run_module_asynchronous()

        # print(f"[ DEBUG ] Engine Result Dictionary : {self.engine_result_dictionary}")
    
    """
    IN : 
    OUT : 
    """
    def create_engine_result(self) :
        # print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        # print(" [ Kernel Service - Engine ] Create Engine Result ...")
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
        # [ 1. ] Set Engine Resource
        self.set_engine_resource()

        # [ 2. ] Load Module
        self.load_module()

        # [ 3. ] Run Module
        self.run_module()

        # [ 4. ] Create Engine Result
        self.create_engine_result()

        return self.engine_result_dictionary
