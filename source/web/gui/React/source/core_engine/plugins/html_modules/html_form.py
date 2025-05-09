# [ Core ] Module - HTML : html_form.py

# Tag - Form ( Password )

from plugins._base_module import BaseModule

import sys
import requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
from urllib.parse import urlparse
import tldextract

class HtmlForm(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.m_form_list = []

    """
    IN : 
    OUT : 
    """
    def get_domain_suffix(self, url) :
        tldextract_result = tldextract.extract(url)

        return f"{tldextract_result.domain}.{tldextract_result.suffix}"

    """
    IN : 
    OUT : 
    """
    def is_external_domain(self, base_url, input_url) :
        base_domain = self.get_domain_suffix(base_url)

        input_domain = self.get_domain_suffix(input_url)

        return base_domain != input_domain

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        headers = {
            "User-Agent" : "Mozilla/5.0"
        }

        try :
            response = requests.get(self.input_url, headers = headers, timeout = 5)

            response.raise_for_status()

            html = response.text

        except requests.RequestException as e :

            self.module_result_flag = False
            self.module_result_data["reason"] = f"Fail to Get HTML."

            self.create_module_result()

            return self.module_result_dictionary

        bs = BeautifulSoup(html, "html.parser")

        base_url = self.input_url

        form_list = bs.find_all("form")

        if not form_list :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Fail to Get Form Tag."

            self.create_module_result()

            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        for form in form_list :

            form_action_data = form.get("action", "")

            form_password_flag = bool(form.find("input", {"type" : "password"}))

            if self.is_external_domain(base_url, form_action_data) and form_password_flag :

                self.module_result_flag = True
                self.module_result_data["reason"] = "Form Tag Use Password to External Domain."
                self.module_result_data["form_action"] = form_action_data

                self.create_module_result()

                # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

                return self.module_result_dictionary

        self.module_result_flag = False
        self.module_result_data["reason"] = "Form Tag Not Use Password to External Domain."

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 html_form.py < URL >")

        sys.exit(1)

    input_url = sys.argv[1]

    module_instance = HtmlForm(input_url)

    module_instance.scan()
