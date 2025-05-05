# [ Core ] Kernel - Kernel Service - Engine : full_scan_engine.py

from engines._base_scan_engine import BaseScanEngine, URL_MODULE_DIRECTORY_PATH, HTML_MODULE_DIRECTORY_PATH, JS_MODULE_DIRECTORY_PATH

# [ Full ]
ENGINE_RESULT_SCORE = 100

class FullScanEngine(BaseScanEngine) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        # [ Full ] Module List
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

        # [ Full ] Module Order List - Synchronous
        self.module_order_list_synchronous = [
            "UrlTinyDomain",
            "UrlHttp",
            "UrlSsl",
        ]

        # [ Full ] Module Order List - Asynchronous
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

        # [ Full ] Module Weight List
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
