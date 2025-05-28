# [ Kernel ] Kernel Service - Engine : _base_scan_engine.py

import importlib
import requests
import asyncio
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

URL_MODULE_DIRECTORY_PATH = "kernel.plugins.url_modules"
HTML_MODULE_DIRECTORY_PATH = "kernel.plugins.html_modules"
JS_MODULE_DIRECTORY_PATH = "kernel.plugins.js_modules"
AI_MODULE_DIRECTORY_PATH = "kernel.plugins.ai_modules"

# 0 ~ 9 : Low Suspicious ( Not Malicious )
# 10 ~ 19 : Suspicious
# 20 ~ 29 : High Suspicious ( Malicious )
LOW_SUSPICIOUS_WEIGHT = 0
SUSPICIOUS_WEIGHT = 10
HIGH_SUSPICIOUS_WEIGHT = 20

# [ Default ]
ENGINE_RESULT_SCORE = 60

class BaseScanEngine :
    def __init__(self, input_url) :
        self.input_url = input_url
        self.redirect_url = None

        self.request_headers = {
            "User-Agent" : (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language" : "en-US, en;q=0.9",
            "Accept" : "text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8",
            "Connection" : "keep-alive",
        }

        self.time_out_module = 10

        self.engine_resource = {}

        # [ Default ] Module List
        self.module_path_list = [
            # Synchronous
            (URL_MODULE_DIRECTORY_PATH, "url_short"),

            # Asynchronous #1 - AI
            (AI_MODULE_DIRECTORY_PATH, "ai_url"),

            # Asynchronous #2 - URL
            (URL_MODULE_DIRECTORY_PATH, "url_homograph"),
            (URL_MODULE_DIRECTORY_PATH, "url_http"),
            (URL_MODULE_DIRECTORY_PATH, "url_ssl"),
            (URL_MODULE_DIRECTORY_PATH, "url_sub_domain"),
            (URL_MODULE_DIRECTORY_PATH, "url_whois"),

            # Asynchronous #3 - HTML
            (HTML_MODULE_DIRECTORY_PATH, "html_form"),
            (HTML_MODULE_DIRECTORY_PATH, "html_iframe"),
            (HTML_MODULE_DIRECTORY_PATH, "html_js_url"),
            (HTML_MODULE_DIRECTORY_PATH, "html_link"),
            (HTML_MODULE_DIRECTORY_PATH, "html_meta_refresh"),
            (HTML_MODULE_DIRECTORY_PATH, "html_resource_url"),
            (HTML_MODULE_DIRECTORY_PATH, "html_style"),

            # Asynchronous #4 - JS Static
            (JS_MODULE_DIRECTORY_PATH, "js_static_external"),
            (JS_MODULE_DIRECTORY_PATH, "js_static_hook"),
            (JS_MODULE_DIRECTORY_PATH, "js_static_obfuscate"),
            (JS_MODULE_DIRECTORY_PATH, "js_static_redirect"),
            (JS_MODULE_DIRECTORY_PATH, "js_static_script"),

            # Asynchronous #5 - JS Dynamic
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
            "AiUrl",

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

            "AiUrl": 0, # Special ( Dynamic )

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
    def get_js_file(self, js_file_url) :
        start_time = time.time()

        try :
            response = requests.get(js_file_url, headers = self.request_headers, timeout = 5)
            
            response.raise_for_status()

            js_file = response.text

            print(f"  [ + ]  {'Get JS File - Success':<25} ( {round(time.time() - start_time, 2)}s : {js_file_url} )")

            return js_file_url, js_file
        
        except Exception as e :

            print(f"  [ ! ]  {'Get JS File - Fail':<25} ( {round(time.time() - start_time, 2)}s : {js_file_url} )")
            print(f"{e}")

            return js_file_url, None
    
    """
    IN : 
    OUT : 
    """
    def set_engine_resource(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Set Engine Resource ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        start_time = time.time()

        try :
            response = requests.get(self.input_url, headers = self.request_headers, timeout = 5)

            response.raise_for_status()

            bs = BeautifulSoup(response.text, "html.parser")

            print(f"  [ + ]  {'Get HTML File - Success':<25} ( {round(time.time() - start_time, 2)}s : {self.input_url} )")

            html_file_script_tag_list = []
            js_file_dictionary = {}

            script_tag_list = bs.find_all("script")

            js_file_url_list = []

            for script_tag in script_tag_list :

                if script_tag.get("src") :

                    js_file_url = urljoin(self.input_url, script_tag["src"])
                    js_file_url_list.append(js_file_url)
                
                else :

                    if script_tag.string :

                        html_file_script_tag_list.append(script_tag.string.strip())

            # Asynchronous : Get JS File
            with ThreadPoolExecutor() as executor :

                work_list = []

                for js_file_url in js_file_url_list :

                    work_list.append(executor.submit(self.get_js_file, js_file_url))

                for work in as_completed(work_list) :

                    js_file_url, js_file = work.result()

                    if js_file :
            
                        js_file_dictionary[js_file_url] = js_file    
                
            self.engine_resource["html_file_bs_object"] = bs
            self.engine_resource["html_file_script_tag_list"] = html_file_script_tag_list
            self.engine_resource["js_file_dictionary_list"] = js_file_dictionary

        # except requests.exceptions.HTTPError as e :
        #     print(f"[ ERROR ] Fail to Set Engine Resource ( Get HTML ) - HTTP ERROR : {self.input_url}")
        #     print(f"{e}")
        
        # except requests.exceptions.RequestException as e :
        #     print(f"[ ERROR ] Fail to Set Engine Resource ( Get HTML ) - Request ERROR : {self.input_url}")
        #     print(f"{e}")
        
        except Exception as e :
            print(f"  [ ! ]  {'Get HTML File - Fail':<25} ( {round(time.time() - start_time, 2)}s : {self.input_url} )")
            print(f"{e}")
        
        # Not Key - Set Default
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
            module_file_path = import_path.replace(".", "/") + ".py" 

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
    async def run_a_module_asynchronous_with_time_out(self, module_instance) :
        start_time = time.time()

        try :
            run_result = await asyncio.wait_for(module_instance.scan(), timeout = self.time_out_module)

            module_run_flag = run_result.get("module_run", False)

            if not module_run_flag :

                module_error_message = run_result.get("module_error", "")

                # ERROR - Time Out "O" in Module Level
                if "time out" in module_error_message.lower() :

                    print("[ DEBUG - Module Level in Engine ] Time Out.")

                    return {
                        "run_status" : "Time Out",
                        "run_time" : round(time.time() - start_time, 2),
                        "run_result" : None,
                        "run_error" : "[ ERROR ] Time Out",

                    }

            # print("[ DEBUG - Engine Level in Engine ] \"Not\" Time Out. ( Run Success )")

            return {
                "run_status" : "Success",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : run_result,
            }
        
        # ERROR - Time Out "O" in Engine Level
        except asyncio.TimeoutError :
            print("[ DEBUG - Engine Level in Engine ] Time Out.")

            return {
                "run_status" : "Time Out",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : None,
                "run_error" : "[ ERROR ] Time Out",

            }
        
        # ERROR - Time Out "X" in Engine Level
        except Exception as e :
            print("[ DEBUG - Engine Level in Engine ] \"Not\" Time Out. ( Run Fail )")

            return {
                "run_status" : "Error",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : None,
                "run_error" : f"[ ERROR ] {e}",
            }

    """
    IN : 
    OUT : 
    """
    async def run_a_module_asynchronous(self, module_instance) :
        module_class_name = module_instance.__class__.__name__

        try :
            run_a_module_with_time_out_result = await self.run_a_module_asynchronous_with_time_out(module_instance)
            
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
    async def run_module_asynchronous(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Service - Engine ] Run Module ( Asynchronous ) ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        task_list = []

        for module_instance in self.module_instance_list :

            module_class_name = module_instance.__class__.__name__

            if module_class_name in self.module_order_list_asynchronous :

                task_list.append(self.run_a_module_asynchronous(module_instance))

        await asyncio.gather(*task_list, return_exceptions = True)
    
    """
    IN : 
    OUT : 
    """
    def run_a_module_synchronous_with_time_out(self, module_instance) :
        start_time = time.time()

        try :
            with ThreadPoolExecutor() as executor :

                work = executor.submit(module_instance.scan)

                run_result = work.result(timeout = self.time_out_module)

            run_result = module_instance.scan()

            module_run_flag = run_result.get("module_run", False)

            if not module_run_flag :

                module_error_message = run_result.get("module_error", "")

                # ERROR - Time Out "O" in Module Level
                if "time out" in module_error_message.lower() :

                    print("[ DEBUG - Module Level in Engine ] Time Out.")

                    return {
                        "run_status" : "Time Out",
                        "run_time" : round(time.time() - start_time, 2),
                        "run_result" : None,
                        "run_error" : "[ ERROR ] Time Out",

                    }

            # print("[ DEBUG - Engine Level in Engine ] \"Not\" Time Out. ( Run Success )")

            return {
                "run_status" : "Success",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : run_result,
            }
        
        # ERROR - Time Out "O" in Engine Level
        except asyncio.TimeoutError :
            print("[ DEBUG - Engine Level in Engine ] Time Out.")

            return {
                "run_status" : "Time Out",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : None,
                "run_error" : "[ ERROR ] Time Out",

            }
        
        # ERROR - Time Out "X" in Engine Level
        except Exception as e :
            print("[ DEBUG - Engine Level in Engine ] \"Not\" Time Out. ( Run Fail )")

            return {
                "run_status" : "Error",
                "run_time" : round(time.time() - start_time, 2),
                "run_result" : None,
                "run_error" : f"[ ERROR ] {e}",
            }

    """
    IN : 
    OUT : 
    """
    def run_a_module_synchronous(self, module_instance) :
        module_class_name = module_instance.__class__.__name__

        try :
            run_a_module_with_time_out_result = self.run_a_module_synchronous_with_time_out(module_instance)
            
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
                
                self.run_a_module_synchronous(module_instance)

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
    def run_module(self) :
        # print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        # print(" [ Kernel Service - Engine ] Run Module ...")
        # print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        self.run_module_synchronous()
        asyncio.run(self.run_module_asynchronous())

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

        ai_run_true_flag = False
        ai_scan_true_flag = False

        ai_run_true_score = 0
        ai_run_true_weight = 0
        
        for module_result_dictionary in self.module_result_dictionary_list :

            module_weight = 0

            module_class_name = module_result_dictionary.get("module_class_name")

            try :
                # AI
                if module_class_name == "AiUrl" :

                    if module_result_dictionary.get("module_run") :

                        ai_run_true_flag = True
                    
                    if module_result_dictionary.get("module_result_flag") :

                        ai_scan_true_flag = True
                
                # ETC ( Not AI )
                else : 

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

        # AI - Run - True
        if ai_run_true_flag :

            # AI : Run - True + Scan - True
            if ai_scan_true_flag :

                ai_run_true_score = run_true_weight
                ai_run_true_weight = run_true_weight
            
            # AI : Run - True + Scan - False
            else :

                ai_run_true_score = 0
                ai_run_true_weight = run_true_weight

        # AI - Run - False
        else :

            ai_run_true_score = 0
            ai_run_true_weight = 0
        
        engine_result_rate_score_weight = ( run_true_score + ai_run_true_score ) / ( run_true_weight + ai_run_true_weight )

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
