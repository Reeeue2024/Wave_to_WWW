# [ Kernel ] Kernel Service - Engine : full_scan_engine.py

from kernel.engines._base_scan_engine import BaseScanEngine, URL_MODULE_DIRECTORY_PATH, HTML_MODULE_DIRECTORY_PATH, JS_MODULE_DIRECTORY_PATH, AI_MODULE_DIRECTORY_PATH

# [ Full ]
ENGINE_RESULT_SCORE = 60

class FullScanEngine(BaseScanEngine) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        # Time Out
        self.time_out_module = 20

        # [ Full ] Module List
        self.module_path_list = [
            (URL_MODULE_DIRECTORY_PATH, "url_short"),

            (AI_MODULE_DIRECTORY_PATH, "ai"),

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

        # [ Full ] Module Order List - Synchronous
        self.module_order_list_synchronous = [
            "UrlShort",
        ]

        # [ Full ] Module Order List - Asynchronous
        self.module_order_list_asynchronous = [
            "Ai",

            "UrlHomograph",
            "UrlHttp",
            "UrlSsl",
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

        # [ Full ] Module Weight List
        self.module_weight_dictionary = {
            "UrlShort" : 5, # LOW

            "Ai": 0, # Special ( Dynamic )

            "UrlHomograph" : 20, # HIGH
            "UrlHttp" : 5, # LOW
            "UrlSsl" : 15, # NOT LOW + NOT HIGH #2
            "UrlSubDomain" : 10,
            "UrlWhois" : 10,

            "HtmlForm" : 15, # NOT LOW + NOT HIGH #2
            "HtmlIframe" : 15, # NOT LOW + NOT HIGH #2
            "HtmlJsUrl" : 10, # NOT LOW + NOT HIGH #1
            "HtmlLink" : 10, # NOT LOW + NOT HIGH #1
            "HtmlMetaRefresh" : 15, # NOT LOW + NOT HIGH #2
            "HtmlResourceUrl" : 10, # NOT LOW + NOT HIGH #1
            "HtmlStyle" : 20, # HIGH ( ? )
            
            "JsStaticExternal" : 10, # NOT LOW + NOT HIGH #1
            "JsStaticHook" : 15, # NOT LOW + NOT HIGH #2
            "JsStaticObfuscate" : 10, # NOT LOW + NOT HIGH #1
            "JsStaticRedirect" : 15, # NOT LOW + NOT HIGH #2
            "JsStaticScript" : 10, # NOT LOW + NOT HIGH #1

            "JsDynamicDom" : 20, # HIGH
            "JsDynamicExternal" : 15, # NOT LOW + NOT HIGH #2
            "JsDynamicHook" : 15, # NOT LOW + NOT HIGH #2
            "JsDynamicObfuscate" : 20, # HIGH
            "JsDynamicRedirect" : 15, # NOT LOW + NOT HIGH #2
        }
