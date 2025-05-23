# [ Kernel ] Kernel Service - Engine : _base_scan_engine.py

import os
import importlib
import requests
import asyncio
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

URL_MODULE_DIRECTORY_PATH = "core_engine.plugins.url_modules"
HTML_MODULE_DIRECTORY_PATH = "core_engine.plugins.html_modules"
JS_MODULE_DIRECTORY_PATH = "core_engine.plugins.js_modules"

# 0 ~ 9 : Low Suspicious ( Not Malicious )
# 10 ~ 19 : Suspicious
# 20 ~ 29 : High Suspicious ( Malicious )
LOW_SUSPICIOUS_WEIGHT = 0
SUSPICIOUS_WEIGHT = 10
HIGH_SUSPICIOUS_WEIGHT = 20

# [ Default ]
ENGINE_RESULT_SCORE = 60

class BaseScanEngine :
    def __init__(self, input_url, time_out_module = 20) :
        self.input_url = input_url
        self.redirect_url = None

        self.time_out_module = time_out_module

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
            (HTML_MODULE_DIRECTORY_PATH, "html_link"),
            (HTML_MODULE_DIRECTORY_PATH, "html_meta_refresh"),
            (HTML_MODULE_DIRECTORY_PATH, "html_resource_url"),
            (HTML_MODULE_DIRECTORY_PATH, "html_style"),

            (JS_MODULE_DIRECTORY_PATH, "js_static_external"),
            (JS_MODULE_DIRECTORY_PATH, "js_static_hook"),
            (JS_MODULE_DIRECTORY_PATH, "js_static_obfuscate"),
            (JS_MODULE_DIRECTORY_PATH, "js_static_redirect"),
            (JS_MODULE_DIRECTORY_PATH, "js_static_script"),

            (JS_MODULE_DIRECTORY_PATH, "js_dynamic_dom"),
            (JS_MODULE_DIRECTORY_PATH, "js_dynamic_external"),
            (JS_MODULE_DIRECTORY_PATH, "js_dynamic_hook"),
            (JS_MODULE_DIRECTORY_PATH, "js_dynamic_obfuscate"),
            (JS_MODULE_DIRECTORY_PATH, "js_dynamic_redirect"),
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
            "HtmlLink",
            "HtmlMetaRefresh",
            "HtmlResourceUrl",
            "HtmlStyle",

            "JsStaticExternal",
            "JsStaticHook",
            "JsStaticObfuscate",
            "JsStaticRedirect",
            "JsStaticScript",

            "JsDynamicDom",
            "JsDynamicExternal",
            "JsDynamicHook",
            "JsDynamicObfuscate",
            "JsDynamicRedirect",
        ]

        self.module_result_dictionary_list = []

        # [ Default ] Module Weight List
        self.module_weight_dictionary = {
            "UrlShort" : 10,

            "UrlHomograph" : 28,
            "UrlHttp" : 12,
            "UrlSsl" : 12,
            "UrlSubDomain" : 12,
            "UrlWhois" : 4,

            "HtmlForm" : 24,
            "HtmlIframe" : 14,
            "HtmlJsUrl" : 14,
            "HtmlLink" : 14,
            "HtmlMetaRefresh" : 24,
            "HtmlResourceUrl" : 14,
            "HtmlStyle" : 4,

            "JsStaticExternal" : 12,
            "JsStaticHook" : 18,
            "JsStaticObfuscate" : 14,
            "JsStaticRedirect" : 18,
            "JsStaticScript" : 12,

            "JsDynamicDom" : 18,
            "JsDynamicExternal" : 14,
            "JsDynamicHook" : 18,
            "JsDynamicObfuscate" : 18,
            "JsDynamicRedirect" : 28,
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
                ),
                "Accept-Language" : "en-US, en;q=0.9",
                "Accept" : "text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8",
                "Connection" : "keep-alive",
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

        except requests.exceptions.HTTPError as e :
            print(f"[ ERROR ] Fail to Set Engine Resource ( Get HTML ) - HTTP ERROR : {self.input_url}")
            print(f"{e}")
        
        except requests.exceptions.RequestException as e :
            print(f"[ ERROR ] Fail to Set Engine Resource ( Get HTML ) - Request ERROR : {self.input_url}")
            print(f"{e}")
        
        except Exception as e :
            print(f"[ ERROR ] Fail to Set Engine Resource : {self.input_url}")
            print(f"{e}")
        
        finally :
            self.engine_resource.setdefault("html_file_bs_object", None)
            self.engine_resource.setdefault("html_file_script_tag_list", None)
            self.engine_resource.setdefault("js_file_dictionary_list", None)
    
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
    def run_a_module_with_time_out(self, module_instance) :
        event_loop = asyncio.new_event_loop()

        asyncio.set_event_loop(event_loop)

        start_time = time.time()

        try :
            run_result = event_loop.run_until_complete(
                asyncio.wait_for(module_instance.scan(), timeout = self.time_out_module)
            )

            return {
                "run_status" : "Success",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : run_result,
            }
        
        # ERROR - Time Out : O
        except asyncio.TimeoutError :
            return {
                "run_status" : "Time Out",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : None,
                "run_error" : "[ ERROR ] Time Out",

            }
        
        # ERROR - Time Out : X
        except Exception as e :
            return {
                "run_status" : "Error",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : None,
                "run_error" : f"[ ERROR ] {e}",
            }
        
        finally :
            try:
                task_list = asyncio.all_tasks(event_loop)

                for task in task_list :

                    task.cancel()

                event_loop.run_until_complete(asyncio.gather(*task_list, return_exceptions = True))

            except Exception as e :
                print(f"[ ERROR ] Fail to Clean Task.")
                print(f"{e}")

            finally :
                event_loop.close()
    
    """
    IN : 
    OUT : 
    """
    def run_a_module(self, module_instance) :
        module_class_name = module_instance.__class__.__name__

        try :
            run_a_module_with_time_out_result = self.run_a_module_with_time_out(module_instance)
            
            module_run_status = run_a_module_with_time_out_result["run_status"]
            module_run_time = run_a_module_with_time_out_result["run_time"]

            if module_run_status == "Success" :

                module_result_dictionary = run_a_module_with_time_out_result["run_result"]

                self.module_result_dictionary_list.append({
                    "module_class_name" : module_class_name,
                    "module_weight" : self.module_weight_dictionary.get(module_class_name),
                    "module_run" : True,
                    "module_result_flag" : module_result_dictionary.get("module_result_flag"),
                    "module_result_data" : module_result_dictionary.get("module_result_data"),
                })

                print(f"  [ + ]  {module_class_name:<25} ( Run Module - {module_run_status} : {module_run_time}s )")

            else :

                self.module_result_dictionary_list.append({
                    "module_class_name" : module_class_name,
                    "module_weight" : self.module_weight_dictionary.get(module_class_name),
                    "module_run" : False,
                    "module_error" : run_a_module_with_time_out_result.get("run_error"),
                    "module_result_flag" : False,
                    "module_result_data" : None,
                })

                print(f"  [ ! ]  {module_class_name:<25} ( Run Module - {module_run_status} : {module_run_time}s )")

        except Exception as e :
            self.module_result_dictionary_list.append({
                "module_class_name" : module_class_name,
                "module_weight" : self.module_weight_dictionary.get(module_class_name),
                "module_run" : False,
                "module_error" : f"{e}",
                "module_result_flag" : False,
                "module_result_data" : None,
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

                        print(f"  ( Redirect By Short URL ) Before URL : {self.input_url}")

                        self.input_url = redirect_url

                        print(f"  ( Redirect By Short URL ) After URL : {self.input_url}")

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

        run_true_score = 0
        run_true_weight = 0
        
        module_result_dictionary_list = []

        high_suspicious_flag = False

        engine_result_rate_score_weight = 0.0
        
        for module_result_dictionary in self.module_result_dictionary_list :

            module_weight = 0

            try :

                if module_result_dictionary.get("module_run") :

                    module_weight = module_result_dictionary.get("module_weight", 0)

                    if module_result_dictionary.get("module_result_flag") :

                        run_true_score += module_weight

                        if module_weight >= HIGH_SUSPICIOUS_WEIGHT :
    
                            high_suspicious_flag = True
                    
                    run_true_weight += module_weight

            except Exception as e :
                print(f"[ ERROR ] Fail to Get Result from Module : \"{module_result_dictionary.get('module_class_name')}\"")
                print(f"{e}")

                module_weight = 0
                    
            try :
                module_result_dictionary_list.append({
                    "module_score" : module_weight,
                    **module_result_dictionary,
                })

            except Exception as e :
                print(f"[ ERROR ] Fail to Set Result Dictionary from Module : \"{module_result_dictionary.get('module_class_name')}\"")
                print(f"{e}")
    
        engine_result_rate_score_weight = run_true_score / run_true_weight

        self.engine_result_score = round(engine_result_rate_score_weight * 100)
        
        if high_suspicious_flag :
            
            self.engine_result_flag = True

        elif self.engine_result_score >= ENGINE_RESULT_SCORE :

            self.engine_result_flag = True

        else :
            
            self.engine_result_flag = False
        
        self.engine_result_dictionary = {
            "engine_result_flag" : self.engine_result_flag,
            "engine_result_score" : self.engine_result_score,
            "engine_result_run_true_score" : run_true_score,
            "engine_result_run_true_weight" : run_true_weight,
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
