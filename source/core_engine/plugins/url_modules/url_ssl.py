# [ Core ] Module - URL : url_ssl.py

from plugins._base_module import BaseModule

import sys
import ssl
import socket
from urllib.parse import urlparse
from cryptography import x509 # pip install cryptography
from cryptography.hazmat.backends import default_backend
import certifi

class UrlSsl(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.certificate = None

        self.free_ca_list = self.get_kernel_resource("ssl_free_ca_list")
        self.low_trust_ca_list = self.get_kernel_resource("ssl_low_trust_ca_list")

    """
    IN : 
    OUT : 
    """
    def get_certificate(self) :
        try :
            urlparse_result = urlparse(self.input_url)
            hostname = urlparse_result.hostname

            ssl_context = ssl.create_default_context(cafile = certifi.where())
            ssl_socket = ssl_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = hostname)
            ssl_socket.settimeout(5)
            ssl_socket.connect((hostname, 443))

            certificate_der = ssl_socket.getpeercert(binary_form = True)
            certificate = x509.load_der_x509_certificate(certificate_der, default_backend())

            return certificate

        except Exception as e :
            return None

    """
    IN : 
    OUT : 
    """
    def scan_free_ca(self) :
        issuer_string = self.certificate.issuer.rfc4514_string()

        # print(f"[ DEBUG ] Issuer ( String ) : {issuer_string}")
        
        for free_ca_element in self.free_ca_list :

            free_ca = free_ca_element.get("free_ca")

            if free_ca and free_ca in issuer_string :

                return True, f"Free CA ( {free_ca} )"
        
        return False, "Not Free CA"

    """
    IN : 
    OUT : 
    """
    def scan_low_trust_ca(self) :
        issuer_string = self.certificate.issuer.rfc4514_string()

        # print(f"[ DEBUG ] Issuer ( String ) : {issuer_string}")

        for low_trust_ca_element in self.low_trust_ca_list :

            low_trust_ca = low_trust_ca_element.get("low_trust_ca")

            if low_trust_ca and low_trust_ca in issuer_string :

                return True, f"Low Trust CA ( {low_trust_ca} )"
        
        return False, "Not Low Trust CA"

    """
    IN : 
    OUT : 
    """
    def scan(self) :
        """
        Not CA => False
        Free CA => True
        Low Trust CA => True
        ETC CA => False
        """

        self.certificate = self.get_certificate()

        if not self.certificate :

            self.module_result_flag = False
            self.module_result_data["reason"] = "Fail to Get SSL Certificate."

            self.create_module_result()

            return self.module_result_dictionary

        free_flag, free_data = self.scan_free_ca()
        low_trust_flag, low_trust_data = self.scan_low_trust_ca()

        self.module_result_data["free_ca"] = free_data
        self.module_result_data["low_trust_ca"] = low_trust_data

        if free_flag or low_trust_flag :

            self.module_result_flag = True
            self.module_result_data["reason"] = "Free CA" if free_flag else "Low Trust CA"

        else :

            self.module_result_flag = False
            self.module_result_data["reason"] = ""
        
        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 url_ssl.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = UrlSsl(input_url)
    
    module_instance.scan()
