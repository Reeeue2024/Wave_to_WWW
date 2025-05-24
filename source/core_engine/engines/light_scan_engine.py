# [ Kernel ] Kernel Service - Engine : light_scan_engine.py

from core_engine.engines._base_scan_engine import BaseScanEngine, URL_MODULE_DIRECTORY_PATH, HTML_MODULE_DIRECTORY_PATH, JS_MODULE_DIRECTORY_PATH, AI_MODULE_DIRECTORY_PATH

# [ Light ]
ENGINE_RESULT_SCORE = 70

class LightScanEngine(BaseScanEngine) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        # [ Light ] Module List
        self.module_path_list = [
            (URL_MODULE_DIRECTORY_PATH, "url_short"),

            (AI_MODULE_DIRECTORY_PATH, "ai_url"),

            # (URL_MODULE_DIRECTORY_PATH, "url_homograph"),
            (URL_MODULE_DIRECTORY_PATH, "url_http"),
            # (URL_MODULE_DIRECTORY_PATH, "url_ssl"),
            (URL_MODULE_DIRECTORY_PATH, "url_sub_domain"),
            # (URL_MODULE_DIRECTORY_PATH, "url_whois"),

            (HTML_MODULE_DIRECTORY_PATH, "html_form"),
            (HTML_MODULE_DIRECTORY_PATH, "html_iframe"),
            (HTML_MODULE_DIRECTORY_PATH, "html_js_url"),
            (HTML_MODULE_DIRECTORY_PATH, "html_link"),
            (HTML_MODULE_DIRECTORY_PATH, "html_meta_refresh"),
            (HTML_MODULE_DIRECTORY_PATH, "html_resource_url"),
            (HTML_MODULE_DIRECTORY_PATH, "html_style"),

            # (JS_MODULE_DIRECTORY_PATH, "js_static_external"),
            # (JS_MODULE_DIRECTORY_PATH, "js_static_hook"),
            # (JS_MODULE_DIRECTORY_PATH, "js_static_obfuscate"),
            # (JS_MODULE_DIRECTORY_PATH, "js_static_redirect"),
            # (JS_MODULE_DIRECTORY_PATH, "js_static_script"),

            # (JS_MODULE_DIRECTORY_PATH, "js_dynamic_dom"),
            # (JS_MODULE_DIRECTORY_PATH, "js_dynamic_external"),
            # (JS_MODULE_DIRECTORY_PATH, "js_dynamic_hook"),
            # (JS_MODULE_DIRECTORY_PATH, "js_dynamic_obfuscate"),
            # (JS_MODULE_DIRECTORY_PATH, "js_dynamic_redirect"),
        ]

        # [ Light ] Module Order List - Synchronous
        self.module_order_list_synchronous = [
            "UrlShort",
        ]

        # [ Light ] Module Order List - Asynchronous
        self.module_order_list_asynchronous = [
            "AiUrl",

            # "UrlHomograph",
            "UrlHttp",
            # "UrlSsl",
            "UrlSubDomain",
            # "UrlWhois",

            "HtmlForm",
            "HtmlIframe",
            "HtmlJsUrl",
            "HtmlLink",
            "HtmlMetaRefresh",
            "HtmlResourceUrl",
            "HtmlStyle",

            # "JsStaticExternal",
            # "JsStaticHook",
            # "JsStaticObfuscate",
            # "JsStaticRedirect",
            # "JsStaticScript",

            # "JsDynamicDom",
            # "JsDynamicExternal",
            # "JsDynamicHook",
            # "JsDynamicObfuscate",
            # "JsDynamicRedirect",
        ]

        # [ Light ] Module Weight List
        self.module_weight_dictionary = {
            "UrlShort" : 10,

            "AiUrl": 0, # Special ( Dynamic )

            # "UrlHomograph" : 10,
            "UrlHttp" : 10,
            # "UrlSsl" : 10,
            "UrlSubDomain" : 10,
            # "UrlWhois" : 10,

            "HtmlForm" : 10,
            "HtmlIframe" : 10,
            "HtmlJsUrl" : 10,
            "HtmlLink" : 10,
            "HtmlMetaRefresh" : 10,
            "HtmlResourceUrl" : 10,
            "HtmlStyle" : 10,

            # "JsStaticExternal" : 10,
            # "JsStaticHook" : 10,
            # "JsStaticObfuscate" : 10,
            # "JsStaticRedirect" : 10,
            # "JsStaticScript" : 10,

            # "JsDynamicDom" : 10,
            # "JsDynamicExternal" : 10,
            # "JsDynamicHook" : 10,
            # "JsDynamicObfuscate" : 10,
            # "JsDynamicRedirect" : 10,
        }
